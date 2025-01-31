import os
import subprocess
import shutil
from pathlib import Path

class RepositoryOperations:
    def __init__(self, logger, error_logger):
        self.logger = logger
        self.error_logger = error_logger

    def clone_repository(self, repo_path, clone_url, token):
        """Clone a repository to the specified path."""
        self.logger.info(f"Repositório local não encontrado, clonando: {repo_path}")
        try:
            clone_process = subprocess.run(
                ['git', 'clone', '--mirror', self._add_token_to_url(clone_url, token), str(repo_path)],
                check=True,
                capture_output=True,
                text=True
            )
            self.logger.info(f"Clone Output: {clone_process.stdout}")
            self.logger.error(f"Clone Error Output: {clone_process.stderr}")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr
            if isinstance(error_msg, bytes):
                error_msg = error_msg.decode()
            error_msg = f"Erro ao clonar repositório: {error_msg}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

    def update_repository(self, repo_path, clone_url, token):
        """Update an existing repository."""
        self.logger.info(f"Repositório local encontrado, atualizando: {repo_path}")
        self.logger.info(f"Verificando se repo_path é um repositório git válido: {repo_path}")
        try:
            # First configure the remote URL with token
            subprocess.run(
                ['git', 'remote', 'set-url', 'origin', self._add_token_to_url(clone_url, token)],
                check=True,
                capture_output=True,
                text=True,
                cwd=str(repo_path)
            )

            git_check_process = subprocess.run(
                ['git', 'rev-parse', '--is-inside-work-tree'],
                cwd=str(repo_path),
                capture_output=True,
                text=True
            )
            if git_check_process.returncode != 0:
                raise Exception("Invalid Git repository")

            fetch_process = subprocess.run(
                ['git', 'fetch', '--all'],
                check=True,
                capture_output=True,
                text=True,
                cwd=str(repo_path)
            )
            self.logger.info(f"Fetch Output: {fetch_process.stdout}")
            self.logger.error(f"Fetch Error Output: {fetch_process.stderr}")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr
            if isinstance(error_msg, bytes):
                error_msg = error_msg.decode()
            error_msg = f"Erro ao fazer fetch do repositório: {error_msg}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

    def push_repository(self, repo_path, clone_url, token):
        """Push all changes to a repository."""
        self.logger.info(f"Executando git push --all e --tags no diretório: {repo_path}")
        try:
            push_process_all = subprocess.run(
                ['git', 'push', '--all', self._add_token_to_url(clone_url, token)],
                check=True,
                capture_output=True,
                text=True,
                cwd=str(repo_path)
            )
            self.logger.info(f"Push All Output: {push_process_all.stdout}")
            self.logger.error(f"Push All Error Output: {push_process_all.stderr}")

            push_process_tags = subprocess.run(
                ['git', 'push', '--tags', self._add_token_to_url(clone_url, token)],
                check=True,
                capture_output=True,
                text=True,
                cwd=str(repo_path)
            )
            self.logger.info(f"Push Tags Output: {push_process_tags.stdout}")
            self.logger.error(f"Push Tags Error Output: {push_process_tags.stderr}")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr
            if isinstance(error_msg, bytes):
                error_msg = error_msg.decode()
            error_msg = f"Erro ao fazer push do repositório: {error_msg}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

    def remove_repository(self, repo_path):
        """Remove a repository directory."""
        self.logger.info(f"Removendo diretório existente: {repo_path}")
        try:
            def onerror(func, path, exc_info):
                self.error_logger.log_error(exc_info[1], f"Erro ao remover arquivo: {path}")
            try:
                subprocess.run(
                    ['rm', '-rf', str(repo_path)] if os.name != 'nt' else ['cmd', '/c', 'rmdir', '/s', '/q', str(repo_path)],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout for large directories
                )
            except subprocess.TimeoutExpired:
                self.error_logger.log_error(TimeoutError(), f"Timeout ao tentar remover {repo_path}")
                raise TimeoutError(f"Timeout ao tentar remover {repo_path}")
        except PermissionError as e:
            error_msg = f"Erro de permissão ao remover diretório: {e}"
            self.error_logger.log_error(e, f"Erro de permissão ao remover {repo_path}: {error_msg}")
            raise Exception(error_msg) from e
        except Exception as e:
            error_msg = f"Erro ao remover diretório: {e}"
            self.error_logger.log_error(e, f"Erro ao remover {repo_path}: {error_msg}")
            raise e

    def _add_token_to_url(self, repo_url, token):
        """Add authentication token to repository URL."""
        from urllib.parse import urlparse, urlunparse
        parsed_url = urlparse(repo_url)
        if token:
            return urlunparse(parsed_url._replace(netloc=f"{token}@{parsed_url.netloc}"))
        return repo_url