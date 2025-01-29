import unittest
import os
from backup_logic.github_operations import GithubOperations
from github import GithubException

class TestGithubIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup logging
        class MockLogger:
            def info(self, msg): print(f"INFO: {msg}")
            def error(self, msg): print(f"ERROR: {msg}")
            def log_error(self, e, msg): print(f"ERROR: {msg} - {str(e)}")
        
        cls.logger = MockLogger()
        cls.error_logger = MockLogger()
        
        # Get tokens from environment variables
        cls.source_token = os.getenv('SOURCE_GITHUB_TOKEN')
        cls.dest_token = os.getenv('DEST_GITHUB_TOKEN')
        
        if not cls.source_token or not cls.dest_token:
            raise unittest.SkipTest("GitHub tokens not found in environment variables")

    def setUp(self):
        self.github_ops = GithubOperations(self.logger, self.error_logger)

    def test_initialization_with_real_tokens(self):
        """Test initialization with real GitHub tokens"""
        try:
            self.github_ops.initialize_clients(self.source_token, self.dest_token)
            self.assertIsNotNone(self.github_ops._source_github)
            self.assertIsNotNone(self.github_ops._dest_github)
            print("✓ Successfully initialized GitHub clients")
        except Exception as e:
            self.fail(f"Failed to initialize with real tokens: {str(e)}")

    def test_list_source_repositories(self):
        """Test listing repositories from source account"""
        self.github_ops.initialize_clients(self.source_token, self.dest_token)
        try:
            repos = self.github_ops.get_source_repos()
            self.assertIsInstance(repos, list)
            print(f"✓ Successfully listed {len(repos)} repositories from source account")
            if repos:
                print(f"  First repo name: {repos[0].name}")
        except Exception as e:
            self.fail(f"Failed to list repositories: {str(e)}")

    def test_get_or_create_test_repo(self):
        """Test repository operations with a test repository"""
        self.github_ops.initialize_clients(self.source_token, self.dest_token)
        
        # Create a mock source repo for testing
        class MockRepo:
            name = "test-backup-repo"
            description = "Test repository for backup operations"
            private = True
            has_issues = True
            has_wiki = True
        
        mock_source_repo = MockRepo()
        
        try:
            dest_repo = self.github_ops.get_or_create_dest_repo(mock_source_repo)
            self.assertIsNotNone(dest_repo)
            print(f"✓ Successfully accessed/created test repository: {dest_repo.name}")
            
            # Test syncing settings
            self.github_ops.sync_repo_settings(mock_source_repo, dest_repo)
            print("✓ Successfully synced repository settings")
            
        except GithubException as e:
            if e.status == 404:
                print("Repository not found (expected for first run)")
            else:
                self.fail(f"GitHub API error: {str(e)}")
        except Exception as e:
            self.fail(f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    unittest.main()