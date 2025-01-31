# GitHub Repository Backup & Mirror Tool

This tool allows you to create backups of your GitHub repositories by mirroring them to another GitHub account. It supports both public and private repositories, preserves all branches and tags, and maintains repository settings.

## Features

- Complete repository mirroring between GitHub accounts
- Preservation of all branches, tags, and commit history
- Maintenance of repository settings (private/public status, description, etc.)
- Resume interrupted backups
- Graphical User Interface (GUI) and Command Line Interface (CLI)
- Pause/resume system with state persistence
- Dynamic disk space verification
- Configurable retry mechanism
- Comprehensive token and permission validation
- Token testing utility

## Prerequisites

1. Python 3.8 or higher
2. Git installed on the system
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

1. Create a `.env` file in the root directory (use `.env.example` as template):
```env
# GitHub Tokens
SOURCE_GITHUB_TOKEN=your_source_account_token
DEST_GITHUB_TOKEN=your_destination_account_token
BACKUP_DIR=C:\path\to\your\backup\directory
```

2. Generate GitHub Personal Access Tokens:
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate tokens for both accounts
   - Required permissions:
     * Source account:
       - `repo` (repository access)
       - `read:org` (organization read)
     * Destination account:
       - `repo` (repository access)
       - `delete_repo` (repository management)

3. Test your tokens using the test utility:
```bash
cd scripts
python test_token.py your_token
```

## Usage

### GUI Mode (Default)

1. Run the application:
```bash
python github_backup.py
```

2. The graphical interface provides:
   - Token validation with detailed feedback
   - Retry count configuration
   - Pause/resume system
   - Real-time monitoring
   - Incremental backup
   - Configuration options

### CLI Mode

1. Run in command line mode:
```bash
python github_backup.py --cli
```

## Project Structure

```
project/
├── backup_logic/           # Core logic
│   ├── __init__.py
│   ├── backup_execution.py
│   ├── disk_space_check.py
│   ├── github_operations.py
│   ├── progress_management.py
│   ├── repository_operations.py
│   ├── token_validation.py
│   └── tests/             # Unit and integration tests
├── scripts/               # Utilities
│   ├── test_token.py     # Token testing tool
│   └── test_token.bat    # Windows wrapper
├── old/                  # Deprecated files
└── docs/                 # Documentation
```

## Security

- Tokens are validated for format and permissions
- Specific scope verification
- Secure subprocess handling
- Atomic file operations
- Log sanitization

## Error Handling

- Disk space verification
- Comprehensive token validation
- Configurable retry count
- Automatic failure recovery
- Detailed error logging

## Running Tests

```bash
# Run all tests
python -m pytest backup_logic/tests/

# Test specific token
python scripts/test_token.py your_token

# Check test coverage
python -m pytest --cov=backup_logic tests/
```

## Troubleshooting

1. Token issues:
   - Use `scripts/test_token.py` for diagnostics
   - Check required scopes
   - Verify organization permissions

2. Backup errors:
   - Check logs in `error_log.log`
   - Adjust retry count
   - Verify disk space

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/feature-name`)
3. Run the tests (`python -m pytest`)
4. Commit your changes
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.