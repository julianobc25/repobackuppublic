# GitHub Backup Manager

Aplicação com interface gráfica para realizar backup automático de repositórios entre contas GitHub.

## Configuração do Ambiente

1. Primeiro, crie e ative um ambiente virtual:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

Ou simplesmente execute o script de configuração automática:
```bash
setup.bat
```

## Sistema de Logs e Tratamento de Erros

### Logs e Relatórios de Erro
- Logs detalhados são salvos em `%APPDATA%\Local\github_backup\logs`
- Cada sessão gera um arquivo de log com timestamp
- Interface visual para visualizar erros em tempo real
- Funcionalidade de copiar erro para área de transferência
- Histórico completo de erros anteriores

### Funcionalidades de Debug
1. **Janela de Erro Detalhada**:
   - Stack trace completo
   - Contexto do erro
   - Data e hora exata
   - Botão para copiar informações

2. **Histórico de Logs**:
   - Visualização de logs anteriores
   - Organização por data/hora
   - Busca e filtro de erros
   - Exportação de logs

3. **Recuperação de Erros**:
   - Sistema automático de pausa em caso de erro
   - Continuação do ponto onde parou
   - Preservação do progresso

### Como Usar o Sistema de Logs

1. **Quando ocorrer um erro**:
   - Uma janela será exibida com detalhes do erro
   - Clique em "Copiar Erro" para copiar as informações
   - Use "Ver Logs Anteriores" para consultar o histórico

2. **Para acessar logs antigos**:
   - Clique em "Ver Logs Anteriores" na janela de erro
   - Navegue pelos arquivos de log organizados por data
   - Use a funcionalidade de cópia para compartilhar

## Tokens do GitHub

### Permissões Necessárias

Para o funcionamento correto do programa, seus tokens precisam ter as seguintes permissões:

#### Token da Conta de Origem:
- `repo` (acesso completo aos repositórios)
  - Permite ler informações dos repositórios
  - Permite clonar repositórios privados

#### Token da Conta de Destino:
- `repo` (acesso completo aos repositórios)
  - Permite criar novos repositórios
  - Permite push para repositórios
  - Permite modificar configurações dos repositórios

### Como Criar os Tokens

1. Acesse GitHub.com
2. Vá em Settings → Developer settings → Personal access tokens → Tokens (classic)
3. Clique em "Generate new token (classic)"
4. Dê um nome ao token (ex: "GitHub Backup Manager")
5. Selecione as permissões mencionadas acima
6. Clique em "Generate token"
7. **IMPORTANTE**: Copie o token imediatamente - você não poderá vê-lo novamente!

## Funcionalidades

- Interface gráfica intuitiva
- Backup completo de todos os repositórios do usuário
- Mirror cloning para preservar todas as branches e tags
- Sistema de pausa e continuação do backup
- Barra de progresso e área de status
- Log detalhado das operações
- Salva progresso automaticamente
- Suporte a arquivo .env para salvar configurações

## Configuração

### 1. Usando arquivo .env (Recomendado)

1. Copie o arquivo de exemplo para criar seu .env:
```bash
cp .env.example .env
```

2. Edite o arquivo .env e adicione seus tokens:
```
SOURCE_GITHUB_TOKEN=seu_token_da_conta_origem
DEST_GITHUB_TOKEN=seu_token_da_conta_destino
BACKUP_DIR=/caminho/personalizado/para/backup  # opcional
```

### 2. Via Interface Gráfica

1. Execute o programa:
```bash
python github_backup.py
```

2. Na interface:
   - Cole os tokens nos campos apropriados
   - Verifique/modifique o diretório de backup
   - Opcional: Marque a opção "Salvar configurações no arquivo .env"
   - Clique em "Iniciar Backup"

## Solução de Problemas

### Erros Comuns

1. **"Token inválido" ou "Permissões insuficientes"**:
   - Verifique se os tokens foram criados com as permissões corretas
   - Gere novos tokens se necessário
   - Confirme se os tokens foram colados corretamente

2. **"Módulo não encontrado"**:
   - Certifique-se que o ambiente virtual está ativado
   - Reinstale as dependências:
     ```bash
     pip install -r requirements.txt
     ```

3. **"Erro ao criar repositório"**:
   - Verifique se a conta de destino tem permissão para criar repositórios
   - Confirme se não atingiu o limite de repositórios privados

4. **"Erro de conexão"**:
   - Verifique sua conexão com a internet
   - Confirme se github.com está acessível

Para ver a versão dos pacotes instalados:
```bash
pip freeze
```

## Observações

- O programa cria automaticamente o diretório de backup se não existir
- Os repositórios já baixados são atualizados automaticamente
- Em caso de erro em um repositório, o programa continua com os próximos
- O progresso é mantido mesmo se o programa for fechado
- As configurações podem ser salvas no .env através da interface