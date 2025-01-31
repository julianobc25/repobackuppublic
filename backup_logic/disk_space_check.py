import os
import shutil
from pathlib import Path
from typing import Tuple

class DiskSpaceChecker:
    def __init__(self, logger, error_logger):
        self.logger = logger
        self.error_logger = error_logger
        self.MIN_BUFFER_SPACE = 2_000_000_000  # 2GB buffer
        
    def estimate_required_space(self, repos) -> int:
        """Estima o espaço necessário para os repositórios.
        
        Args:
            repos: Lista de repositórios a serem clonados
            
        Returns:
            int: Espaço estimado necessário em bytes
        """
        total_size = 0
        for repo in repos:
            # Usa o tamanho do repo + 20% de margem para operações
            repo_size = repo.size * 1024  # Convert KB to bytes
            total_size += repo_size * 1.2
        
        # Adiciona buffer mínimo
        return int(total_size) + self.MIN_BUFFER_SPACE

    def get_disk_space(self, path: str) -> Tuple[int, int, int]:
        """Obtém informações de espaço em disco.
        
        Args:
            path: Caminho para verificar
            
        Returns:
            Tuple[int, int, int]: (total, usado, livre) em bytes
            
        Raises:
            ValueError: Se o caminho for inválido
            OSError: Se houver erro ao acessar o disco
        """
        if not path:
            raise ValueError("Caminho não pode ser vazio")
            
        path = Path(path)
        if not path.exists():
            raise ValueError(f"Caminho não existe: {path}")
            
        try:
            total, used, free = shutil.disk_usage(str(path))
            self.logger.info(f"Espaço em disco para {path}:")
            self.logger.info(f"Total: {total / 1e9:.2f}GB")
            self.logger.info(f"Usado: {used / 1e9:.2f}GB")
            self.logger.info(f"Livre: {free / 1e9:.2f}GB")
            return total, used, free
        except OSError as e:
            raise OSError(f"Erro ao verificar espaço em disco: {e}")

    def check_disk_space(self, path: str, required_space: int = None) -> bool:
        """Verifica se há espaço em disco suficiente.
        
        Args:
            path: Caminho a ser verificado
            required_space: Espaço necessário em bytes (opcional)
            
        Returns:
            bool: True se tiver espaço suficiente
            
        Raises:
            ValueError: Se o caminho for inválido
            Exception: Se não houver espaço suficiente
        """
        try:
            if not path:
                raise ValueError("Caminho não pode ser vazio")

            # Verifica se o caminho existe ou pode ser criado
            path = Path(path)
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
                
            # Obtém informações de espaço
            total, used, free = self.get_disk_space(str(path))
            
            # Se não foi especificado espaço requerido, usa buffer mínimo
            if required_space is None:
                required_space = self.MIN_BUFFER_SPACE
                
            # Verifica se há espaço suficiente
            if free < required_space:
                required_gb = required_space / 1e9
                free_gb = free / 1e9
                raise Exception(
                    f"Espaço insuficiente em disco. "
                    f"Necessário {required_gb:.2f}GB, "
                    f"disponível {free_gb:.2f}GB"
                )
                
            self.logger.info(
                f"Verificação de espaço em disco concluída. "
                f"Espaço livre suficiente: {free / 1e9:.2f}GB"
            )
            return True
            
        except OSError as e:
            self.error_logger.log_error(
                e, 
                f"Erro ao verificar espaço em disco em: {path}"
            )
            raise
        except Exception as e:
            self.error_logger.log_error(
                e,
                f"Erro ao verificar espaço em disco em: {path}"
            )
            raise