#!/usr/bin/env python3
import sys
import json
import requests
from github import Github
from pathlib import Path

def test_token(token):
    """Test a GitHub token and display its permissions and scopes."""
    print("\n=== Teste de Token GitHub ===\n")
    
    # Verifica formato do token
    if not token.strip():
        print("❌ Erro: Token vazio")
        return False
        
    # Testa acesso básico à API
    try:
        response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'token {token}'}
        )
        
        print("== Informações Básicas ==")
        if response.status_code == 200:
            user_data = response.json()
            print(f"✓ Login: {user_data['login']}")
            print(f"✓ Tipo: {user_data['type']}")
            if 'plan' in user_data and user_data['plan']:
                print(f"✓ Plano: {user_data['plan']['name']}")
        else:
            print(f"❌ Erro de autenticação: {response.status_code}")
            return False
            
        print("\n== Escopos do Token ==")
        if 'X-OAuth-Scopes' in response.headers:
            scopes = [s.strip() for s in response.headers['X-OAuth-Scopes'].split(',') if s.strip()]
            for scope in scopes:
                print(f"✓ {scope}")
        else:
            print("ℹ️ Token parece ser um token de acesso pessoal clássico")
            
        # Testa permissões específicas
        print("\n== Teste de Permissões ==")
        g = Github(token)
        user = g.get_user()
        
        # Teste de repos privados
        try:
            private_repos = list(user.get_repos(type='private'))
            print(f"✓ Acesso a repos privados: {len(private_repos)} encontrados")
        except Exception as e:
            print(f"❌ Sem acesso a repos privados: {str(e)}")
            
        # Teste de organizações
        try:
            orgs = list(user.get_orgs())
            print(f"✓ Acesso a organizações: {len(orgs)} encontradas")
            for org in orgs:
                print(f"  - {org.login}")
        except Exception as e:
            print(f"❌ Sem acesso a organizações: {str(e)}")
            
        # Teste de limites de API
        try:
            rate_limit = g.get_rate_limit()
            print(f"\n== Limites de API ==")
            print(f"✓ Core: {rate_limit.core.remaining}/{rate_limit.core.limit}")
            print(f"✓ Search: {rate_limit.search.remaining}/{rate_limit.search.limit}")
        except Exception as e:
            print(f"❌ Erro ao verificar limites de API: {str(e)}")
            
        # Testa criação/deleção de repo
        print("\n== Teste de Criação/Deleção ==")
        try:
            print("Tentando criar repositório de teste...")
            repo = user.create_repo(
                'temp-test-token-repo',
                description='Repositório temporário para teste de token',
                private=True,
                auto_init=True
            )
            print("✓ Criação de repositório: OK")
            
            print("Tentando deletar repositório de teste...")
            repo.delete()
            print("✓ Deleção de repositório: OK")
        except Exception as e:
            print(f"❌ Sem permissão para criar/deletar repos: {str(e)}")
            
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao testar token: {str(e)}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Uso: python test_token.py <github_token>")
        print("  ou: python test_token.py --env para usar token do arquivo .env")
        sys.exit(1)
        
    token = sys.argv[1]
    
    if token == '--env':
        try:
            from dotenv import load_dotenv
            import os
            load_dotenv()
            token = os.getenv('GITHUB_TOKEN')
            if not token:
                print("❌ Erro: Token não encontrado no arquivo .env")
                print('Adicione GITHUB_TOKEN=seu_token no arquivo .env')
                sys.exit(1)
        except ImportError:
            print("❌ Erro: python-dotenv não instalado")
            print("Execute: pip install python-dotenv")
            sys.exit(1)
    
    success = test_token(token)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()