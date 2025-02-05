import os
from github import Github
import requests
from dotenv import load_dotenv

def test_token(token, token_type):
    print(f"\nTesting {token_type} token...")
    
    # Test with requests first
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('https://api.github.com/user', headers=headers)
    print(f"Direct API call status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        print(f"User data: {response.json().get('login')}")
    else:
        print(f"Error response: {response.text}")

    # Test with PyGithub
    try:
        g = Github(token)
        user = g.get_user()
        print(f"PyGithub test - User login: {user.login}")
        print(f"Rate limit remaining: {g.get_rate_limit().core.remaining}")
    except Exception as e:
        print(f"PyGithub test failed: {str(e)}")

def main():
    load_dotenv()
    
    source_token = os.getenv('SOURCE_GITHUB_TOKEN', '').strip()
    dest_token = os.getenv('DEST_GITHUB_TOKEN', '').strip()
    
    if not source_token or not dest_token:
        print("Error: Missing tokens in .env file")
        return
    
    test_token(source_token, "source")
    test_token(dest_token, "destination")

if __name__ == "__main__":
    main()