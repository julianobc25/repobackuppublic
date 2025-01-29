from github import Github
from github.GithubException import BadCredentialsException

def validate_token(token):
    try:
        g = Github(token)
        g.get_user().login
        return True
    except BadCredentialsException:
        return False
