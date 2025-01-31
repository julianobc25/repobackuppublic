from github import Github
from github.GithubException import BadCredentialsException, GithubException
import re
import requests

REQUIRED_SCOPES = {
    'source': ['repo', 'read:org'],
    'dest': ['repo', 'delete_repo']
}

def _validate_token_format(token):
    """Validate token format matches GitHub's pattern."""
    if not token or not isinstance(token, str):
        return False
    # GitHub tokens are 40 hex chars for classic or start with ghp_ for fine-grained
    return bool(re.match(r'^(ghp_[a-zA-Z0-9]{36}|[a-f0-9]{40})$', token))

def _check_rate_limits(github_client, logger):
    """Check if the token has sufficient API rate limits."""
    try:
        rate_limit = github_client.get_rate_limit()
        core_remaining = rate_limit.core.remaining
        logger.info(f"Rate limit remaining: {core_remaining}")
        if core_remaining < 100:  # Ensure enough calls available
            raise Exception(f"Taxa limite da API muito baixa: {core_remaining} chamadas restantes")
        return True
    except GithubException as e:
        raise Exception(f"Erro ao verificar limites de API: {str(e)}")

def _validate_scopes(token, required_scopes, token_type):
    """Validate if token has required scopes using GitHub API."""
    try:
        response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'token {token}'}
        )
        
        if 'X-OAuth-Scopes' not in response.headers:
            raise Exception(f"Token {token_type} não possui escopos OAuth")
            
        scopes = [s.strip() for s in response.headers['X-OAuth-Scopes'].split(',')]
        missing_scopes = [s for s in required_scopes if s not in scopes]
        
        if missing_scopes:
            raise Exception(
                f"Token {token_type} não possui os escopos necessários: {', '.join(missing_scopes)}"
            )
            
        return True
    except requests.RequestException as e:
        raise Exception(f"Erro ao validar escopos do token {token_type}: {str(e)}")

def validate_token(token):
    """Basic token validation for UI checks."""
    try:
        if not _validate_token_format(token):
            return False
            
        g = Github(token)
        g.get_user().login
        return True
    except BadCredentialsException:
        return False
    except Exception:
        return False

def validate_tokens(source_token, dest_token, logger, error_logger):
    """Valida os tokens e permissões das contas GitHub

    Verifica se os tokens de origem e destino são válidos e se a conta
    de destino tem todas as permissões necessárias
    """
    try:
        # Valida formato dos tokens
        if not _validate_token_format(source_token):
            raise Exception("Token de origem em formato inválido")
        if not _validate_token_format(dest_token):
            raise Exception("Token de destino em formato inválido")

        # Valida token de origem
        source_github = Github(source_token.strip())
        try:
            source_user = source_github.get_user()
            source_user.id
            _check_rate_limits(source_github, logger)
            _validate_scopes(source_token, REQUIRED_SCOPES['source'], 'origem')
            logger.info(f"Token de origem validado para usuário: {source_user.login}")
        except Exception as e:
            raise Exception(f"Erro na validação do token de origem: {str(e)}")

        # Valida token de destino
        dest_github = Github(dest_token.strip())
        try:
            dest_user = dest_github.get_user()
            dest_user.id
            _check_rate_limits(dest_github, logger)
            _validate_scopes(dest_token, REQUIRED_SCOPES['dest'], 'destino')
            logger.info(f"Token de destino validado para usuário: {dest_user.login}")
            
            # Testa permissões específicas na conta destino
            private_repos = list(dest_user.get_repos(type='private'))
            logger.info("Permissão de leitura de repos privados verificada")
            
            # Tenta criar um repo de teste temporário
            try:
                test_repo = dest_user.create_repo(
                    'temp-permission-test-repo',
                    private=True,
                    auto_init=True
                )
                test_repo.delete()
                logger.info("Permissão de criação/deleção de repos verificada")
            except GithubException as e:
                raise Exception(f"Sem permissão para criar/deletar repos: {str(e)}")

            user_data = dest_github.get_user().raw_data
            if 'plan' in user_data and user_data['plan']:
                logger.info("Permissões verificadas na conta de destino")
            else:
                raise Exception("Conta de destino não tem plano que permite repositórios privados")

        except Exception as e:
            raise Exception(f"Erro na validação do token de destino: {str(e)}")

        return True

    except Exception as e:
        error_logger.log_error(e, "Erro na validação dos tokens")
        raise