# Estrutura do Projeto (Project Structure)

Este documento detalha a estrutura e função de cada arquivo no projeto.

## Arquivos Principais (Main Files)

### `github_backup.py`
- Arquivo principal do programa
- Contém as implementações do modo GUI e CLI
- Gerencia a interface do usuário e o fluxo principal do programa
- Responsável por iniciar o processo de backup

### `requirements.txt`
- Lista todas as dependências do projeto
- Inclui versões específicas das bibliotecas necessárias
- Usado para instalar dependências via pip

### `.env`
- Arquivo de configuração com variáveis de ambiente
- Armazena tokens do GitHub e diretório de backup
- Não versionado (incluído no .gitignore)

### `README.md`
- Documentação principal em Português
- Instruções de instalação e uso
- Descrição das funcionalidades

### `README_EN.md`
- Documentação em Inglês
- Mesma estrutura do README.md
- Referência cruzada com a versão em Português

## Diretório `backup_logic/`
Contém a lógica principal do programa, dividida em módulos especializados.

### `backup_logic/__init__.py`
- Marca o diretório como um pacote Python
- Disponibiliza as classes principais para importação

### `backup_logic/backup_execution.py`
- Classe `BackupExecutor`
- Orquestra o processo de backup
- Gerencia o fluxo de execução e tratamento de erros
- Coordena as operações de repositório e GitHub

### `backup_logic/github_operations.py`
- Classe `GithubOperations`
- Gerencia todas as interações com a API do GitHub
- Responsável por operações como:
  * Inicialização de clientes GitHub
  * Listagem de repositórios
  * Criação/atualização de repositórios
  * Sincronização de configurações

### `backup_logic/repository_operations.py`
- Classe `RepositoryOperations`
- Gerencia operações Git locais
- Lida com:
  * Clonagem de repositórios
  * Atualização de repositórios
  * Push de alterações
  * Remoção de repositórios

### `backup_logic/token_validation.py`
- Funções de validação de tokens
- Verifica permissões das contas
- Testa acesso aos repositórios

### `backup_logic/disk_space_check.py`
- Verifica espaço em disco disponível
- Previne falhas por falta de espaço
- Gerencia requisitos de armazenamento

### `backup_logic/progress_management.py`
- Gerencia o progresso do backup
- Mantém registro de repositórios processados
- Permite retomada de backups interrompidos

## Diretório `backup_logic/tests/`
Contém todos os testes do projeto.

### `backup_logic/tests/__init__.py`
- Marca o diretório como um pacote Python de testes
- Permite importação dos testes

### `backup_logic/tests/run_tests.py`
- Script para execução de todos os testes
- Configura ambiente de teste
- Gera relatórios de teste

### `backup_logic/tests/test_github_operations.py`
- Testes unitários para `GithubOperations`
- Usa mocks para simular API do GitHub
- Testa diferentes cenários de operação

### `backup_logic/tests/test_github_integration.py`
- Testes de integração
- Testa interação real com API do GitHub
- Verifica fluxo completo de backup

## Arquivos de Log e Monitoramento

### `github_backup.log`
- Registro detalhado de operações
- Inclui informações de tempo e status
- Útil para debugging e monitoramento

### `error_log.log`
- Registro específico de erros
- Detalhes de exceções e falhas
- Auxilia na resolução de problemas

## Arquivos de Interface Gráfica

### `gui_components.py`
- Implementação da interface gráfica
- Usa tkinter para widgets
- Define layout e comportamento da GUI
- Contém:
  * Campos de entrada para tokens
  * Barra de progresso
  * Área de status
  * Botões de controle

## Arquivos de Configuração

### `.gitignore`
- Lista arquivos ignorados pelo Git
- Exclui:
  * Arquivos de ambiente (.env)
  * Logs
  * Cache Python
  * Diretórios virtuais

### `.env.example`
- Modelo para arquivo .env
- Demonstra formato correto
- Lista variáveis necessárias

## Arquivos de Estado

### `backup_progress.json`
- Mantém estado do backup
- Lista repositórios processados
- Permite retomada de operações
- Armazena timestamps de backup

## Como os Componentes se Relacionam

1. O `github_backup.py` inicia o programa e carrega a interface apropriada (GUI/CLI)
2. A interface usa `BackupExecutor` para gerenciar o processo
3. `BackupExecutor` coordena:
   - `GithubOperations` para interações com GitHub
   - `RepositoryOperations` para operações Git locais
   - `progress_management` para rastreamento
4. Logs são mantidos durante todo o processo
5. Testes verificam cada componente individualmente e em conjunto

Este design modular permite:
- Fácil manutenção
- Testabilidade
- Extensibilidade
- Separação clara de responsabilidades