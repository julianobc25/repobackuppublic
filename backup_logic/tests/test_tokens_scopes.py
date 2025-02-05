import os
from github import Github
import requests
from dotenv import load_dotenv

def test_token_scopes(token, token_type):
    print(f"\nTesting {token_type} token scopes...")
    
    # Test with requests first
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # First try to get user info
    response = requests.get('https://api.github.com/user', headers=headers)
    print(f"Status code: {response.status_code}")
    
    # Check for OAuth scopes in response headers
    print("\nResponse Headers:")
    for header, value in response.headers.items():
        if 'x-oauth' in header.lower() or 'x-ratelimit' in header.lower():
            print(f"{header}: {value}")
            
    # If we got an error, print the detailed error message
    if response.status_code != 200:
        try:
            error_json = response.json()
            print("\nError Details:")
            print(f"Message: {error_json.get('message', 'No message')}")
            print(f"Documentation URL: {error_json.get('documentation_url', 'No URL')}")
        except:
            print("Raw response:", response.text)
            
    # Try to list private repos to test repo scope
    print("\nTesting repository access:")
    response = requests.get('https://api.github.com/user/repos?type=private', headers=headers)
    print(f"Private repos access status: {response.status_code}")
    
    if response.status_code == 200:
        repos = response.json()
        print(f"Can access {len(repos)} private repositories")

def main():
    load_dotenv()
    
    source_token = os.getenv('SOURCE_GITHUB_TOKEN', '').strip()
    dest_token = os.getenv('DEST_GITHUB_TOKEN', '').strip()
    
    if not source_token or not dest_token:
        print("Error: Missing tokens in .env file")
        return
    
    test_token_scopes(source_token, "source")
    test_token_scopes(dest_token, "destination")

if __name__ == "__main__":
    main()