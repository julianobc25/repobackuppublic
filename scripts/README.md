# Scripts de Utilitários

## Test Token (test_token.py)

Script para testar tokens do GitHub e verificar suas permissões e escopos.

### Uso

```bash
python test_token.py <github_token>
```

Ou usando token do arquivo .env:

```bash
python test_token.py --env
```

### Funcionalidades

O script verifica:

1. **Informações Básicas**
   - Login do usuário
   - Tipo de conta
   - Plano (se disponível)

2. **Escopos do Token**
   - Lista todos os escopos atribuídos ao token
   - Identifica se é um token clássico ou fino

3. **Permissões Específicas**
   - Acesso a repositórios privados
   - Acesso a organizações
   - Permissões de criação/deleção de repositórios

4. **Limites de API**
   - Taxa de limite core
   - Taxa de limite de busca

### Exemplos de Saída

```
=== Teste de Token GitHub ===

== Informações Básicas ==
✓ Login: username
✓ Tipo: User
✓ Plano: pro

== Escopos do Token ==
✓ repo
✓ read:org
✓ delete_repo

== Teste de Permissões ==
✓ Acesso a repos privados: 10 encontrados
✓ Acesso a organizações: 2 encontradas
  - org1
  - org2

== Limites de API ==
✓ Core: 4999/5000
✓ Search: 30/30

== Teste de Criação/Deleção ==
✓ Criação de repositório: OK
✓ Deleção de repositório: OK
```

### Códigos de Retorno

- 0: Teste concluído com sucesso
- 1: Erro durante o teste

### Requisitos

- Python 3.6+
- Pacotes:
  - PyGithub
  - requests
  - python-dotenv (opcional, para usar arquivo .env)

### Arquivo .env (opcional)

Para usar com a opção --env, crie um arquivo .env com:

```
GITHUB_TOKEN=seu_token_aqui