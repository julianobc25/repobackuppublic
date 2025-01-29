# GitHub Repository Backup Tool

This tool allows you to create backups of your GitHub repositories by mirroring them to another GitHub account. It supports both public and private repositories, preserves all branches and tags, and maintains repository settings.

## Features

- Mirror repositories from one GitHub account to another
- Preserve all branches, tags, and commit history
- Maintain repository settings (private/public status, description, etc.)
- Resume interrupted backups
- Track backup progress
- Handle large repositories with retry mechanisms
- Detailed logging of operations
- Graphical User Interface (GUI) and Command Line Interface (CLI) support
- Pause/Resume functionality (GUI mode)

## Prerequisites

1. Python 3.8 or higher
2. Git installed on your system
3. Two GitHub accounts:
   - Source account (where your repositories are)
   - Destination account (where backups will be stored)
4. Personal access tokens for both accounts

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/github-backup-tool.git
cd github-backup-tool
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory with the following content:
```env
# GitHub Tokens
SOURCE_GITHUB_TOKEN=your_source_account_token
DEST_GITHUB_TOKEN=your_destination_account_token
BACKUP_DIR=C:\path\to\your\backup\directory
```

2. Generate GitHub Personal Access Tokens:
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate tokens for both source and destination accounts
   - Required permissions:
     * `repo` (Full control of private repositories)
     * `workflow` (Update GitHub Action workflows)
     * `read:org` (Read organization data)

## Usage

### GUI Mode (Default)

1. Run the application:
```bash
python github_backup.py
```

2. The GUI will open with the following features:
   - Input fields for source and destination tokens
   - Backup directory selection
   - Option to save configuration to .env file
   - Start/Pause buttons
   - Progress bar
   - Status log window

### CLI Mode

1. Run in command-line mode:
```bash
python github_backup.py --cli
```

2. The tool will:
   - Read configuration from .env file
   - Validate your tokens
   - Create the backup directory if it doesn't exist
   - List all repositories in the source account
   - Mirror each repository to the destination account
   - Show progress as it works
   - Provide a summary of completed and skipped repositories

## Output Directory Structure

```
backup_directory/
├── repo1/              # Bare Git repository
├── repo2/              # Bare Git repository
└── ...
```

## Logs and Progress

- Operation logs are stored in `github_backup.log`
- Error logs are stored in `error_log.log`
- Backup progress is tracked in `backup_progress.json`

## Error Handling

The tool handles various scenarios:
- Network interruptions (with automatic retries)
- Repository access issues
- Invalid tokens
- Rate limiting
- Repository not found errors

If a repository fails to backup after 3 retries, it will be skipped and listed in the final summary.

## Running Tests

The project includes both unit tests and integration tests:

```bash
# Run all tests
python -m backup_logic.tests.run_tests

# Run specific test file
python -m unittest backup_logic/tests/test_github_operations.py
```

## Troubleshooting

1. "Token validation failed":
   - Check if your tokens have the required permissions
   - Verify tokens are correctly set in .env file

2. "Repository not found":
   - Verify the repository exists in source account
   - Check if your token has access to the repository

3. "Rate limit exceeded":
   - Wait for a few minutes and try again
   - GitHub API has rate limits that reset hourly

4. "Push rejected":
   - Check if destination account has enough private repository slots
   - Verify destination token has repository creation permissions

## GUI Features

1. Token Management:
   - Input fields for both source and destination tokens
   - Option to save tokens to .env file for future use

2. Backup Control:
   - Start/Stop backup process
   - Pause/Resume ongoing backups
   - Real-time progress bar

3. Status Monitoring:
   - Scrollable status window showing current operations
   - Error messages and warnings
   - Success confirmations

## Security Notes

- Keep your .env file secure and never commit it to version control
- Tokens should be treated as sensitive credentials
- Use tokens with minimum required permissions
- Regularly rotate your tokens for better security

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.