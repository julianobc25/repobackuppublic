from github import Github
from github.GithubException import BadCredentialsException

def validate_token(token):
    try:
        g = Github(token)
        g.get_user().login
        return True
    except BadCredentialsException:
        return False
    def validate_tokens(self):
        """Valida os tokens e permissões das contas GitHub

        Verifica se os tokens de origem e destino são válidos e se a conta
        de destino tem permissões de leitura e escrita em repositórios privados
        """
        try:
            # Valida token de origem
            source_github = Github(self.gui_components.source_token_entry.get().strip())
            source_user = source_github.get_user()
            source_user.id  # Testa se o token é válido

            # Valida token de destino
            dest_github = Github(self.gui_components.dest_token_entry.get().strip())
            dest_user = dest_github.get_user()
            dest_user.id  # Testa se o token é válido

            # Testa permissões básicas na conta destino
            try:
                # Verifica se pode listar repositórios privados
                private_repos = list(dest_user.get_repos(type='private'))

                # Verifica permissões de criação testando uma API endpoint
                user_data = dest_github.get_user().raw_data
                if 'plan' in user_data and user_data['plan']:
                    self.logger.info("Permissões verificadas na conta de destino")
                else:
                    raise Exception("Conta de destino não tem plano que permite repositórios privados")

                return True

            except GithubException as e:
                raise Exception(f"Token de destino não tem permissões suficientes: {str(e)}")

            except BadCredentialsException as e:
                self.error_logger.log_error(e, "Credenciais inválidas")
                return False
            except Exception as e:
                self.error_logger.log_error(e, "Erro na validação dos tokens")
                return False
        except Exception as e:  # Add
            self.error_logger.log_error(e, "Erro na validação dos tokens")
            return False