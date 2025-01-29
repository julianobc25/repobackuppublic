import shutil

def check_disk_space(path):
    total, used, free = shutil.disk_usage(path)
    return total, used, free

    def check_disk_space(self, path: str) -> bool:
        """Verifica se há espaço em disco suficiente

        Verifica se o caminho informado tem pelo menos 1GB livre.

        Args:
            path (str): Caminho a ser verificado

        Returns:
            bool: True se tiver espaço suficiente, False caso contrário
        """
        try:
            if path is None:
                raise ValueError("Caminho não pode ser nulo")

            total, used, free = shutil.disk_usage(path)
            # Requer pelo menos 1GB livre
            if free < 1_000_000_000:
                raise Exception(f"Espaço insuficiente em disco. Necessário pelo menos 1GB livre.")
            return True
        except OSError as e:
            self.error_logger.log_error(e, f"Erro ao verificar espaço em disco em: {path}")
            return False
        except Exception as e:
            self.error_logger.log_error(e, f"Erro ao verificar espaço em disco em: {path}")
            return False