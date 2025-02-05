from github import Github
from github.GithubException import BadCredentialsException, GithubException
import re
import requests

# Mapeamento de escopos necessários para permissões
REQUIRED_SCOPES = {
    'source': {
        'repo': ['repo', 'public_repo'],  # aceita repo completo ou apenas public_repo
        'org': ['read:org', 'admin:org', 'write:org']  # qualquer nível de acesso org é suficiente
    },
    'dest': {
        'repo': ['repo', 'public_repo'],
        'delete': ['delete_repo', 'repo']  # repo full inclui delete_repo
    }
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

def _has_required_scope(scopes, required_options):
    """Check if any of the required scope options is present."""
    return any(scope in scopes for scope in required_options)

def _validate_scopes(token, required_scopes, token_type, logger):
    """Validate if token has required scopes using GitHub API."""
    try:
        # Primeiro tenta obter os escopos via API
        response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'Bearer {token}'}
        )
        response.raise_for_status()

        # Obtém os escopos do cabeçalho
        if 'X-OAuth-Scopes' in response.headers:
            # Get scopes from header first
            logger.info(f'Headers: {response.headers}')
            scopes = [s.strip() for s in response.headers['X-OAuth-Scopes'].split(',') if s.strip()]
            logger.info(f"Escopos encontrados para token {token_type}: {', '.join(scopes)}")
        else:
            # Se não houver cabeçalho de escopos, pode ser um token de acesso pessoal
            scopes = ['repo']  # Assume acesso total para tokens clássicos
            logger.info(f"Token {token_type} parece ser um token de acesso pessoal clássico")

        # Verifica cada tipo de permissão necessária
        missing_permissions = []

        for perm_type, scope_options in required_scopes.items():
            if not _has_required_scope(scopes, scope_options):
                missing_permissions.append(perm_type)

        if missing_permissions:
            # Se encontrou permissões faltando, tenta validar através de chamadas API específicas
            try:
                # Testa acesso a repositórios
                if 'repo' in missing_permissions:
                    g = Github(token)
                    # Tenta listar repositórios privados
                    list(g.get_user().get_repos(type='private'))
                    missing_permissions.remove('repo')
                    logger.info(f"Token {token_type} tem acesso a repositórios confirmado via API")
             # Testa acesso a organizações
                if 'org' in missing_permissions:
                    g = Github(token)
                    # Tenta listar organizações
                    list(g.get_user().get_orgs())
                    missing_permissions.remove('org')
                    logger.info(f"Token {token_type} tem acesso a organizações confirmado via API")
             # Testa permissão de deleção
                if 'delete' in missing_permissions and token_type == 'destino':
                    g = Github(token)
                    user = g.get_user()
                    # Tenta criar e deletar um repo de teste
                    repo = user.create_repo('temp-test-delete-repo', auto_init=True, private=True)
                    repo.delete()
                    missing_permissions.remove('delete')
                    logger.info(f"Token {token_type} tem permissão de deleção confirmada via API")
            except Exception as e:
                logger.info(f"Erro ao verificar permissões via API para {token_type}: {str(e)}")

        if missing_permissions:
            missing_scopes = []
            for perm in missing_permissions:
                missing_scopes.extend(required_scopes[perm])
            raise Exception(
                f"Token {token_type} não possui as permissões necessárias: {', '.join(set(missing_scopes))}"
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
            source_scopes = REQUIRED_SCOPES['source'].copy()
            _validate_scopes(source_token, source_scopes, 'origem', logger)
            logger.info(f"Token de origem validado para usuário: {source_user.login}")
        except Exception as e:
            raise Exception(f"Erro na validação do token de origem: {str(e)}")

        # Valida token de destino
        dest_github = Github(dest_token.strip())
        try:
            dest_user = dest_github.get_user()
            dest_user.id
            _check_rate_limits(dest_github, logger)
            _validate_scopes(dest_token, REQUIRED_SCOPES['dest'], 'destino', logger)
            logger.info(f"Token de destino validado para usuário: {dest_user.login}")
         # Testa permissões específicas na conta destino
            private_repos = list(dest_user.get_repos(type='private'))
            logger.info("Permissão de leitura de repos privados verificada")

            # Verifica plano do usuário
            user_data = dest_github.get_user().raw_data
            if 'plan' in user_data and user_data['plan']:
                logger.info("Permissões verificadas na conta de destino")
            else:
                logger.info("Aviso: Não foi possível verificar o plano da conta de destino")

        except Exception as e:
            raise Exception(f"Erro na validação do token de destino: {str(e)}")

        return True

    except Exception as e:
        # Log the error but also re-raise it so callers can handle it
        error_logger.log_error(e, "Erro na validação dos tokens")
        logger.error(f"Detalhes do erro de validação: {str(e)}")
        # Re-raise with more specific error message
        raise Exception(f"Erro na validação dos tokens: {str(e)}")
