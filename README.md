# Ferramenta de Backup e Mirror de Repositórios GitHub

Esta ferramenta permite criar backups dos seus repositórios GitHub espelhando-os em outra conta GitHub. Suporta repositórios públicos e privados, preserva todos os branches e tags, e mantém as configurações dos repositórios.

[English Version](README_EN.md)

## Funcionalidades

- Espelhamento completo de repositórios entre contas GitHub
- Preservação de todos os branches, tags e histórico de commits
- Manutenção das configurações dos repositórios (status privado/público, descrição, etc.)
- Retomada de backups interrompidos
- Interface Gráfica (GUI) e Interface de Linha de Comando (CLI)
- Sistema de pausa/retomada com persistência de estado
- Verificação de espaço em disco dinâmica
- Mecanismo configurável de tentativas
- Validação abrangente de tokens e permissões
- Utilitário de teste de tokens

## Pré-requisitos

1. Python 3.8 ou superior
2. Git instalado no sistema
3. Duas contas GitHub:
   - Conta de origem (onde estão seus repositórios)
   - Conta de destino (onde serão armazenados os backups)
4. Tokens de acesso pessoal para ambas as contas

## Instalação

1. Clone este repositório:
```bash
git clone https://github.com/yourusername/github-backup-tool.git
cd github-backup-tool
```

2. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

## Configuração

1. Crie um arquivo `.env` no diretório raiz (use `.env.example` como modelo):
```env
# Tokens do GitHub
SOURCE_GITHUB_TOKEN=seu_token_conta_origem
DEST_GITHUB_TOKEN=seu_token_conta_destino
BACKUP_DIR=C:\caminho\para\seu\diretorio\backup
```

2. Gere Tokens de Acesso Pessoal do GitHub:
   - Vá para Configurações do GitHub > Configurações do desenvolvedor > Tokens de acesso pessoal
   - Gere tokens para ambas as contas
   - Permissões necessárias:
     * Conta de origem:
       - `repo` (acesso a repositórios)
       - `read:org` (leitura de organizações)
     * Conta de destino:
       - `repo` (acesso a repositórios)
       - `delete_repo` (gerenciamento de repositórios)

3. Teste seus tokens usando o utilitário de teste:
```bash
cd scripts
python test_token.py seu_token
```

## Uso

### Modo GUI (Padrão)

1. Execute a aplicação:
```bash
python github_backup.py
```

2. A interface gráfica oferece:
   - Validação de tokens com feedback detalhado
   - Configuração do número de tentativas
   - Sistema de pausa/retomada
   - Monitoramento em tempo real
   - Backup incremental
   - Opções de configuração

### Modo CLI

1. Execute no modo linha de comando:
```bash
python github_backup.py --cli
```

## Estrutura do Projeto

```
projeto/
├── backup_logic/           # Lógica principal
│   ├── __init__.py
│   ├── backup_execution.py
│   ├── disk_space_check.py
│   ├── github_operations.py
│   ├── progress_management.py
│   ├── repository_operations.py
│   ├── token_validation.py
│   └── tests/             # Testes unitários e de integração
├── scripts/               # Utilitários
│   ├── test_token.py     # Ferramenta de teste de tokens
│   └── test_token.bat    # Wrapper para Windows
├── old/                  # Arquivos deprecados
└── docs/                 # Documentação
```

## Segurança

- Tokens são validados quanto a formato e permissões
- Verificação de escopos específicos
- Tratamento seguro de subprocessos
- Operações atômicas de arquivo
- Sanitização de logs

## Tratamento de Erros

- Verificação de espaço em disco
- Validação abrangente de tokens
- Número configurável de tentativas
- Recuperação automática de falhas
- Logs detalhados de erros

## Executando Testes

```bash
# Executar todos os testes
python -m pytest backup_logic/tests/

# Testar token específico
python scripts/test_token.py seu_token

# Verificar cobertura de testes
python -m pytest --cov=backup_logic tests/
```

## Resolução de Problemas

1. Problemas com tokens:
   - Use `scripts/test_token.py` para diagnóstico
   - Verifique os escopos necessários
   - Confirme as permissões de organização

2. Erros de backup:
   - Verifique os logs em `error_log.log`
   - Ajuste o número de tentativas
   - Verifique o espaço em disco

## Contribuindo

1. Faça um fork do repositório
2. Crie sua branch de feature (`git checkout -b feature/nome-do-recurso`)
3. Execute os testes (`python -m pytest`)
4. Faça commit das mudanças
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.