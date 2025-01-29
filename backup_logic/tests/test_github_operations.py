import unittest
from unittest.mock import Mock, patch, PropertyMock
from backup_logic.github_operations import GithubOperations
from github import Github, GithubException

class TestGithubOperations(unittest.TestCase):
    def setUp(self):
        self.logger = Mock()
        self.error_logger = Mock()
        self.github_ops = GithubOperations(self.logger, self.error_logger)

    @patch('backup_logic.github_operations.Github')
    def test_initialize_clients(self, MockGithub):
        # Arrange
        source_token = "source_test_token"
        dest_token = "dest_test_token"
        mock_source_user = Mock()
        mock_dest_user = Mock()
        
        mock_github_instance = Mock()
        mock_github_instance.get_user.return_value = mock_source_user
        MockGithub.return_value = mock_github_instance
        
        # Act
        self.github_ops.initialize_clients(source_token, dest_token)
        
        # Assert
        MockGithub.assert_any_call(source_token)
        MockGithub.assert_any_call(dest_token)
        self.assertIsNotNone(self.github_ops._source_github)
        self.assertIsNotNone(self.github_ops._dest_github)

    @patch('github.Github')
    def test_get_source_repos(self, mock_github):
        # Arrange
        mock_source_user = Mock()
        mock_repos = [Mock(), Mock()]
        mock_source_user.get_repos.return_value = mock_repos
        self.github_ops._source_user = mock_source_user
        
        # Act
        repos = self.github_ops.get_source_repos()
        
        # Assert
        self.assertEqual(repos, mock_repos)
        mock_source_user.get_repos.assert_called_once()

    def test_get_source_repos_without_initialization(self):
        # Act & Assert
        with self.assertRaises(ValueError):
            self.github_ops.get_source_repos()

    @patch('github.Github')
    def test_get_or_create_dest_repo_existing(self, MockGithub):
        # Arrange
        mock_dest_user = Mock()
        mock_source_repo = Mock()
        # Set name as a property
        type(mock_source_repo).name = PropertyMock(return_value="test-repo")
        mock_dest_repo = Mock()
        
        mock_github_instance = Mock()
        mock_github_instance.get_user.return_value = mock_dest_user
        mock_dest_user.get_repo.return_value = mock_dest_repo
        MockGithub.return_value = mock_github_instance
        
        self.github_ops._dest_user = mock_dest_user
        self.github_ops._dest_github = mock_github_instance
        
        # Act
        result = self.github_ops.get_or_create_dest_repo(mock_source_repo)
        
        # Assert
        self.assertEqual(result, mock_dest_repo)
        mock_dest_user.get_repo.assert_called_with("test-repo")
        self.logger.info.assert_called_with("Repositório destino já existe: test-repo")

    @patch('github.Github')
    def test_get_or_create_dest_repo_new(self, MockGithub):
        # Arrange
        mock_dest_user = Mock()
        mock_source_repo = Mock()
        # Set properties using PropertyMock
        type(mock_source_repo).name = PropertyMock(return_value="test-repo")
        type(mock_source_repo).description = PropertyMock(return_value="test description")
        type(mock_source_repo).private = PropertyMock(return_value=True)
        
        mock_dest_repo = Mock()
        
        mock_github_instance = Mock()
        mock_github_instance.get_user.return_value = mock_dest_user
        mock_dest_user.get_repo.side_effect = GithubException(404, "Not Found")
        mock_dest_user.create_repo.return_value = mock_dest_repo
        MockGithub.return_value = mock_github_instance
        
        self.github_ops._dest_user = mock_dest_user
        self.github_ops._dest_github = mock_github_instance
        
        # Act
        result = self.github_ops.get_or_create_dest_repo(mock_source_repo)
        
        # Assert
        self.assertEqual(result, mock_dest_repo)
        mock_dest_user.create_repo.assert_called_with(
            "test-repo",
            description="test description",
            private=True
        )
        self.logger.info.assert_called_with("Criado novo repositório destino: test-repo")

    def test_sync_repo_settings(self):
        # Arrange
        mock_source_repo = Mock()
        # Set properties using PropertyMock
        type(mock_source_repo).name = PropertyMock(return_value="test-repo")
        type(mock_source_repo).description = PropertyMock(return_value="test description")
        type(mock_source_repo).private = PropertyMock(return_value=True)
        type(mock_source_repo).has_issues = PropertyMock(return_value=True)
        type(mock_source_repo).has_wiki = PropertyMock(return_value=True)
        
        mock_dest_repo = Mock()
        
        # Act
        self.github_ops.sync_repo_settings(mock_source_repo, mock_dest_repo)
        
        # Assert
        mock_dest_repo.edit.assert_called_with(
            description="test description",
            private=True,
            has_issues=True,
            has_wiki=True
        )
        self.logger.info.assert_called_with("Configurações sincronizadas para: test-repo")

    def test_sync_repo_settings_error(self):
        # Arrange
        mock_source_repo = Mock()
        type(mock_source_repo).name = PropertyMock(return_value="test-repo")
        mock_dest_repo = Mock()
        mock_dest_repo.edit.side_effect = GithubException(500, "Error")
        
        # Act & Assert
        with self.assertRaises(GithubException):
            self.github_ops.sync_repo_settings(mock_source_repo, mock_dest_repo)
            
        self.error_logger.log_error.assert_called()

if __name__ == '__main__':
    unittest.main()