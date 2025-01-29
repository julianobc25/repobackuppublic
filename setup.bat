@echo off
echo Configurando ambiente para GitHub Backup Manager...
echo.

:: Verifica se Python está instalado
python --version > nul 2>&1
if errorlevel 1 (
    echo Python nao encontrado! Por favor, instale o Python e tente novamente.
    pause
    exit /b 1
)

:: Cria ambiente virtual
echo Criando ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo Erro ao criar ambiente virtual!
    pause
    exit /b 1
)

:: Ativa ambiente virtual e instala dependências
echo Instalando dependencias...
call venv\Scripts\activate
pip install -r requirements.txt
if errorlevel 1 (
    echo Erro ao instalar dependencias!
    pause
    exit /b 1
)

:: Cria arquivo .env se não existir
if not exist .env (
    echo Criando arquivo .env...
    copy .env.example .env
)

echo.
echo Configuracao concluida com sucesso!
echo Para iniciar o programa:
echo 1. Configure seus tokens no arquivo .env
echo 2. Execute: python github_backup.py
echo.
pause