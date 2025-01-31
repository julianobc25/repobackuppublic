@echo off
echo Testando token GitHub...
python test_token.py %*
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Teste concluido com sucesso!
) else (
    echo.
    echo Erro no teste de token!
)
pause