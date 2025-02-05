import os
from dotenv import load_dotenv
import re

def verify_token_format(token, token_type):
    print(f"\nVerifying {token_type} token:")
    print(f"Token length: {len(token)}")
    print(f"Starts with 'ghp_': {token.startswith('ghp_')}")
    print(f"Contains only valid characters: {bool(re.match(r'^ghp_[a-zA-Z0-9]{36}$', token))}")
    
    # Check for common issues
    print("Checking for issues:")
    if len(token) != 40:  # ghp_ (4) + 36 chars
        print(f"- Invalid length (should be 40, got {len(token)})")
    if '\n' in token or '\r' in token:
        print("- Contains newline characters")
    if ' ' in token:
        print("- Contains spaces")
    
    # Print first and last few characters
    if len(token) > 10:
        print(f"Token starts with: {token[:8]}...")
        print(f"Token ends with: ...{token[-8:]}")

def main():
    load_dotenv()
    
    source_token = os.getenv('SOURCE_GITHUB_TOKEN', '')
    dest_token = os.getenv('DEST_GITHUB_TOKEN', '')
    
    if not source_token or not dest_token:
        print("Error: Missing tokens in .env file")
        return
    
    verify_token_format(source_token, "source")
    verify_token_format(dest_token, "destination")

if __name__ == "__main__":
    main()