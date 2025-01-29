import os
import subprocess
from datetime import datetime
from pathlib import Path
from github import Github, GithubException
from tkinter import messagebox
import shutil
import time

print("Script de backup iniciado")

class BackupExecutor:
    def __init__(self, logger, error_logger, progress_manager):
        self.logger = logger
        self.error_logger = error_logger
        self.progress_manager = progress_manager
        self.is_running = False
        self.pause_event = None

    def run_backup(self, source_token, dest_token, backup_dir, progress_var, is_running, pause_event):
        self.is_running = is_running
        self.pause_event = pause_event
        try:
            source_github = Github(source_token)
            dest_github = Github(dest_token)
            backup_path = Path(backup_dir)
            backup_path.mkdir(parents=True, exist_ok=True)

            print(f"Backup path: {backup_path}")
            print(f"Backup path exists: {backup_path.exists()}")
            print(f"Backup path is directory: {backup_path.is_dir()}")

            source_user = source_github.get_user()
            dest_user = dest_github.get_user()
            repos = list(source_user.get_repos())
            total_repos = len(repos)

            self.logger.info(f"Iniciando backup/mirror de {total_repos} repositórios do usuário: {source_user.login}")

            for i, repo in enumerate(repos, 1):
                if not self.is_running or (self.pause_event and self.pause_event.is_set()):
                    break

                if repo.full_name in self.progress_manager.current_progress:
                    self.logger.info(f"Pulando {repo.name} - já foi feito backup anteriormente")
                    continue

                try:
                    self.mirror_repository(repo, backup_path, dest_user, dest_github)
                    self.progress_manager.current_progress[repo.full_name] = datetime.now().isoformat()
                    self.progress_manager.save_progress()

                    progress = (i / total_repos) * 100
                    progress_var.set(progress)

                except Exception as e:
                    self.logger.error(f"Erro no mirror do repositório {repo.name}: {str(e)}")
                    raise e

            if self.is_running and not (self.pause_event and self.pause_event.is_set()):
                self.logger.info("Mirror concluído com sucesso!")
                messagebox.showinfo("Sucesso", "Mirror concluído com sucesso!")

        except Exception as e:
            self.error_logger.log_error(e, "Erro durante o processo de mirror")

    def mirror_repository(self, source_repo, backup_path, dest_user, dest_github):
        self.logger.info(f"Iniciando atualização do repositório: {source_repo.name}")
        self.logger.info(f"Backup path: {backup_path}")
        self.logger.info(f"Repo name: {source_repo.name}")
        repo_path = backup_path / source_repo.name

        print(f"Repo path: {repo_path}")
        print(f"Repo path exists: {repo_path.exists()}")
        print(f"Repo path is directory: {repo_path.is_dir()}")

        if not repo_path.exists():
            self.logger.info(f"Repositório local não encontrado, clonando: {repo_path}")
            try:
                clone_process = subprocess.run(
                    ['git', 'clone', '--mirror', source_repo.clone_url, str(repo_path)],
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
                raise Exception(error_msg) from e
        else:
            self.logger.info(f"Repositório local encontrado, atualizando: {repo_path}")
            self.logger.info(f"Verificando se repo_path é um repositório git válido: {repo_path}")
            try:
                git_check_process = subprocess.run(
                    ['git', 'rev-parse', '--is-inside-work-tree'],
                    cwd=str(repo_path),
                    capture_output=True,
                    text=True
                )
                if git_check_process.returncode != 0:
                    self.logger.error(f"Diretório {repo_path} não é um repositório Git válido. Removendo e clonando novamente.")
                    self._remove_local_repo_directory(repo_path)
                    clone_process = subprocess.run(
                        ['git', 'clone', '--mirror', source_repo.clone_url, str(repo_path)],
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    self.logger.info(f"Clone Output: {clone_process.stdout}")
                    self.logger.error(f"Clone Error Output: {clone_process.stderr}")

                fetch_process = subprocess.run(
                    ['git', 'fetch'],
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
                raise Exception(error_msg) from e

        # Push all changes to the destination repository
        try:
            dest_repo = None
            try:
                dest_repo = dest_github.get_user().get_repo(source_repo.name)
                self.logger.info(f"Repositório destino já existe: {source_repo.name}")
            except GithubException:
                dest_repo = dest_user.create_repo(
                    source_repo.name,
                    description=source_repo.description or "",
                    private=source_repo.private
                )

            self.logger.info(f"Executando git push --all e --tags no diretório: {repo_path}")
            push_process_all = subprocess.run(
                ['git', 'push', '--all', dest_repo.clone_url],
                check=True,
                capture_output=True,
                text=True,
                cwd=str(repo_path)
            )
            self.logger.info(f"Push All Output: {push_process_all.stdout}")
            self.logger.error(f"Push All Error Output: {push_process_all.stderr}")

            push_process_tags = subprocess.run(
                ['git', 'push', '--tags', dest_repo.clone_url],
                check=True,
                capture_output=True,
                text=True,
                cwd=str(repo_path)
            )
            self.logger.info(f"Push Tags Output: {push_process_tags.stdout}")
            self.logger.error(f"Push Tags Error Output: {push_process_tags.stderr}")


            dest_repo.edit(
                description=source_repo.description,
                private=source_repo.private,
                has_issues=source_repo.has_issues,
                has_wiki=source_repo.has_wiki,
                has_downloads=source_repo.has_downloads
            )

            self.logger.info(f"Update concluído com sucesso para: {source_repo.name}")

        except Exception as e:
            self.logger.error(f"Erro durante o push para o repositório destino: {e}")
            raise e

    def _remove_local_repo_directory(self, repo_path):
        self.logger.info(f"Removendo diretório existente: {repo_path}")
        try:
            def onerror(func, path, exc_info):
                self.error_logger.log_error(exc_info[1], f"Erro ao remover arquivo: {path}")
            os.system(f'rmdir /s /q "{repo_path}"')
            shutil.rmtree(repo_path, onerror=onerror, ignore_errors=True)
        except PermissionError as e:
            error_msg = f"Erro de permissão ao remover diretório: {e}"
            self.error_logger.log_error(e, f"Erro de permissão ao remover {repo_path}: {error_msg}")
            raise Exception(error_msg) from e
        except Exception as e:
            error_msg = f"Erro ao remover diretório: {e}"
            self.error_logger.log_error(e, f"Erro ao remover {repo_path}: {error_msg}")
            raise e
