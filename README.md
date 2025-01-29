# Ferramenta de Backup de Repositórios GitHub

Esta ferramenta permite criar backups dos seus repositórios GitHub espelhando-os em outra conta GitHub. Suporta repositórios públicos e privados, preserva todos os branches e tags, e mantém as configurações dos repositórios.

[English Version](README_EN.md)

## Funcionalidades

- Espelhamento de repositórios de uma conta GitHub para outra
- Preservação de todos os branches, tags e histórico de commits
- Manutenção das configurações dos repositórios (status privado/público, descrição, etc.)
- Retomada de backups interrompidos
- Acompanhamento do progresso
- Tratamento de repositórios grandes com mecanismo de tentativas
- Registro detalhado de operações
- Interface Gráfica (GUI) e Interface de Linha de Comando (CLI)
- Funcionalidade de Pausar/Retomar (modo GUI)

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

1. Crie um arquivo `.env` no diretório raiz com o seguinte conteúdo:
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
     * `repo` (Controle total de repositórios privados)
     * `workflow` (Atualização de workflows do GitHub Action)
     * `read:org` (Leitura de dados da organização)

## Uso

### Modo GUI (Padrão)

1. Execute a aplicação:
```bash
python github_backup.py
```

2. A interface gráfica abrirá com os seguintes recursos:
   - Campos para tokens de origem e destino
   - Seleção do diretório de backup
   - Opção para salvar configuração no arquivo .env
   - Botões Iniciar/Pausar
   - Barra de progresso
   - Janela de registro de status

### Modo CLI

1. Execute no modo linha de comando:
```bash
python github_backup.py --cli
```

2. A ferramenta irá:
   - Ler configuração do arquivo .env
   - Validar seus tokens
   - Criar o diretório de backup se não existir
   - Listar todos os repositórios na conta de origem
   - Espelhar cada repositório para a conta de destino
   - Mostrar o progresso conforme trabalha
   - Fornecer um resumo dos repositórios completos e pulados

## Estrutura do Diretório de Saída

```
diretorio_backup/
├── repo1/              # Repositório Git bare
├── repo2/              # Repositório Git bare
└── ...
```

## Logs e Progresso

- Logs de operação são armazenados em `github_backup.log`
- Logs de erro são armazenados em `error_log.log`
- Progresso do backup é rastreado em `backup_progress.json`

## Tratamento de Erros

A ferramenta lida com vários cenários:
- Interrupções de rede (com tentativas automáticas)
- Problemas de acesso ao repositório
- Tokens inválidos
- Limitação de taxa
- Erros de repositório não encontrado

Se um repositório falhar no backup após 3 tentativas, será pulado e listado no resumo final.

## Executando Testes

O projeto inclui testes unitários e de integração:

```bash
# Executar todos os testes
python -m backup_logic.tests.run_tests

# Executar arquivo de teste específico
python -m unittest backup_logic/tests/test_github_operations.py
```

## Resolução de Problemas

1. "Falha na validação do token":
   - Verifique se seus tokens têm as permissões necessárias
   - Verifique se os tokens estão corretamente definidos no arquivo .env

2. "Repositório não encontrado":
   - Verifique se o repositório existe na conta de origem
   - Verifique se seu token tem acesso ao repositório

3. "Limite de taxa excedido":
   - Aguarde alguns minutos e tente novamente
   - A API do GitHub tem limites de taxa que são redefinidos a cada hora

4. "Push rejeitado":
   - Verifique se a conta de destino tem slots suficientes para repositórios privados
   - Verifique se o token de destino tem permissões para criar repositórios

## Recursos da Interface Gráfica

1. Gerenciamento de Tokens:
   - Campos de entrada para tokens de origem e destino
   - Opção para salvar tokens no arquivo .env para uso futuro

2. Controle de Backup:
   - Iniciar/Parar processo de backup
   - Pausar/Retomar backups em andamento
   - Barra de progresso em tempo real

3. Monitoramento de Status:
   - Janela de status rolável mostrando operações atuais
   - Mensagens de erro e avisos
   - Confirmações de sucesso

## Notas de Segurança

- Mantenha seu arquivo .env seguro e nunca o envie para o controle de versão
- Tokens devem ser tratados como credenciais sensíveis
- Use tokens com as permissões mínimas necessárias
- Faça rotação regular dos seus tokens para melhor segurança

## Contribuindo

1. Faça um fork do repositório
2. Crie sua branch de feature (`git checkout -b feature/recurso-incrivel`)
3. Faça commit de suas mudanças (`git commit -m 'Adiciona recurso incrível'`)
4. Faça push para a branch (`git push origin feature/recurso-incrivel`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.