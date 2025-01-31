import os
from datetime import datetime
from pathlib import Path
from github import GithubException
from .token_validation import validate_tokens
from .repository_operations import RepositoryOperations
from .github_operations import GithubOperations

class BackupExecutor:
    def __init__(self, logger, error_logger, progress_manager):
        self.logger = logger
        self.error_logger = error_logger
        self.progress_manager = progress_manager
        self.is_running = False
        self.pause_event = None
        self._source_token = None
        self._dest_token = None
        self.repo_ops = RepositoryOperations(logger, error_logger)
        self.github_ops = GithubOperations(logger, error_logger)

    def run_backup(self, source_token, dest_token, backup_dir, progress_var, is_running, pause_event, cancel_event, retry_count):
        """Execute the backup process for all repositories."""
        self.is_running = is_running
        self.pause_event = pause_event
        self.cancel_event = cancel_event
        try:
            self._setup_tokens(source_token, dest_token)
            self._validate_tokens()
            
            backup_path = self._setup_backup_directory(backup_dir)
            self.github_ops.initialize_clients(self._source_token, self._dest_token)

            ignored_repos = self._load_ignored_repos()
            repos = self.github_ops.get_source_repos()
            repos_to_backup = [repo for repo in repos if repo.name not in ignored_repos]
            total_repos = len(repos_to_backup)
            self.logger.info(f"Iniciando backup/mirror de {total_repos} repositórios (ignorando {len(ignored_repos)} repositórios)")

            skipped_repos = []
            for i, repo in enumerate(repos_to_backup, 1):
                if self._should_stop_processing():
                    break

                if self._is_repo_already_processed(repo):
                    continue

                try:
                    self._process_repository(repo, backup_path, i, total_repos, progress_var, retry_count)
                except GithubException as e:
                    if e.status == 404:
                        self.logger.error(f"Repositório não encontrado, pulando: {repo.name}")
                        skipped_repos.append((repo.name, "Repositório não encontrado"))
                    else:
                        self.logger.error(f"Erro de API do GitHub para {repo.name}: {str(e)}")
                        skipped_repos.append((repo.name, f"Erro de API: {str(e)}"))
                    continue
                except Exception as e:
                    self.logger.error(f"Erro ao processar {repo.name}: {str(e)}")
                    skipped_repos.append((repo.name, str(e)))
                    continue

            if skipped_repos:
                self.logger.info("\nRepositórios pulados:")
                for repo_name, reason in skipped_repos:
                    self.logger.info(f"- {repo_name}: {reason}")

            if self.is_running and not (self.pause_event and self.pause_event.is_set()):
                self.logger.info("Mirror concluído com sucesso!")

        except Exception as e:
            self.error_logger.log_error(e, "Erro durante o processo de mirror")
        except Exception as e:
            self.error_logger.log_error(e, "Erro durante o processo de mirror")
            raise e

    def _load_ignored_repos(self):
        """Load ignored repositories from ignored_repos.txt."""
        ignored_repos = []
        try:
            with open("ignored_repos.txt", "r") as f:
                for line in f:
                    repo_name = line.strip()
                    if repo_name:
                        ignored_repos.append(repo_name)
        except FileNotFoundError:
            pass  # It's okay if the file doesn't exist yet
        return ignored_repos

    def _setup_tokens(self, source_token, dest_token):
        """Setup source and destination tokens."""
        self._source_token = source_token or os.environ.get('SOURCE_GITHUB_TOKEN')
        self._dest_token = dest_token or os.environ.get('DEST_GITHUB_TOKEN')

        if not self._source_token:
            raise ValueError("Source GitHub token is missing. Please provide it as an argument or set the SOURCE_GITHUB_TOKEN environment variable.")
        if not self._dest_token:
            raise ValueError("Destination GitHub token is missing. Please provide it as an argument or set the DEST_GITHUB_TOKEN environment variable.")

    def _validate_tokens(self):
        """Validate both tokens have necessary permissions."""
        if not validate_tokens(self._source_token, self._dest_token, self.logger, self.error_logger):
            raise ValueError("Token validation failed. Please check your tokens and permissions.")

    def _setup_backup_directory(self, backup_dir):
        """Create and verify backup directory."""
        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)
        return backup_path

    def _should_stop_processing(self):
        """Check if processing should be stopped."""
        return not self.is_running or (self.pause_event and self.pause_event.is_set())

    def _is_repo_already_processed(self, repo):
        """Check if repository was already processed."""
        if repo.full_name in self.progress_manager.current_progress:
            self.logger.info(f"Pulando {repo.name} - já foi feito backup anteriormente")
            return True
        return False

    def _process_repository(self, repo, backup_path, current_index, total_repos, progress_var, max_retries=3):
        """Process a single repository."""
        retry_count = 0
        
        self.logger.info(f"\nProcessando repositório {current_index}/{total_repos}: {repo.name}")
        
        while retry_count < max_retries:
            try:
                self._mirror_repository(repo, backup_path)
                self.progress_manager.current_progress[repo.full_name] = datetime.now().isoformat()
                self.progress_manager.save_progress()
                self.logger.info(f"✓ Backup concluído para: {repo.name}")
                break
            except Exception as e:
                retry_count += 1
                self.logger.error(f"Erro no mirror do repositório {repo.name} (tentativa {retry_count}/{max_retries}): {str(e)}")
                if retry_count == max_retries:
                    self.logger.error(f"Número máximo de tentativas ({max_retries}) alcançado para {repo.name}")
                    raise

        self._update_progress(current_index, total_repos, progress_var)

    def _mirror_repository(self, source_repo, backup_path):
        """Mirror a repository to the destination."""
        repo_path = backup_path / source_repo.name
        
        try:
            # Check if repository exists and is accessible
            try:
                source_repo.get_contents("/")
            except GithubException as e:
                if e.status == 404:
                    raise GithubException(404, f"Repository {source_repo.name} is not accessible or has been deleted")
                raise

            if not repo_path.exists():
                self.repo_ops.clone_repository(repo_path, source_repo.clone_url, self._source_token)
            else:
                try:
                    self.repo_ops.update_repository(repo_path, source_repo.clone_url, self._source_token)
                except Exception as e:
                    self.logger.error(f"Erro ao atualizar repositório, tentando clonar novamente: {e}")
                    self.repo_ops.remove_repository(repo_path)
                    self.repo_ops.clone_repository(repo_path, source_repo.clone_url, self._source_token)

            dest_repo = self.github_ops.get_or_create_dest_repo(source_repo)
            self.repo_ops.push_repository(repo_path, dest_repo.clone_url, self._dest_token)
            self.github_ops.sync_repo_settings(source_repo, dest_repo)

        except Exception as e:
            self.logger.error(f"Erro durante o mirror do repositório {source_repo.name}: {str(e)}")
            raise

    def _update_progress(self, current_index, total_repos, progress_var):
        """Update progress bar."""
        if progress_var:
            progress = (current_index / total_repos) * 100
            progress_var.set(progress)
