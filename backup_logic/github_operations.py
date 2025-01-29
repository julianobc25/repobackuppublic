from github import Github, GithubException

class GithubOperations:
    def __init__(self, logger, error_logger):
        self.logger = logger
        self.error_logger = error_logger
        self._source_github = None
        self._dest_github = None
        self._source_user = None
        self._dest_user = None

    def initialize_clients(self, source_token, dest_token):
        """Initialize GitHub clients with the provided tokens."""
        self._source_github = Github(source_token)
        self._dest_github = Github(dest_token)
        self._source_user = self._source_github.get_user()
        self._dest_user = self._dest_github.get_user()

    def get_source_repos(self):
        """Get list of repositories from source account."""
        if not self._source_user:
            raise ValueError("Source GitHub client not initialized")
        return list(self._source_user.get_repos())

    def get_or_create_dest_repo(self, source_repo):
        """Get or create a repository in the destination account."""
        if not self._dest_user:
            raise ValueError("Destination GitHub client not initialized")

        try:
            dest_repo = self._dest_github.get_user().get_repo(source_repo.name)
            self.logger.info(f"Repositório destino já existe: {source_repo.name}")
        except GithubException:
            dest_repo = self._dest_user.create_repo(
                source_repo.name,
                description=source_repo.description or "",
                private=source_repo.private
            )
            self.logger.info(f"Criado novo repositório destino: {source_repo.name}")

        return dest_repo

    def sync_repo_settings(self, source_repo, dest_repo):
        """Synchronize repository settings between source and destination."""
        try:
            dest_repo.edit(
                description=source_repo.description,
                private=source_repo.private,
                has_issues=source_repo.has_issues,
                has_wiki=source_repo.has_wiki
            )
            self.logger.info(f"Configurações sincronizadas para: {source_repo.name}")
        except GithubException as e:
            self.error_logger.log_error(e, f"Erro ao sincronizar configurações do repositório {source_repo.name}")
            raise