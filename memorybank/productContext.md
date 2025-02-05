# Product Context

This document serves as a high-level overview of the product. It includes the project's goals, target audience, and any key decisions made during the project's development.

## Goals
- Ensure robust backup and mirroring of GitHub repositories.
- Support both public and private repositories.
- Preserve all branches, tags, and commit history.
- Maintain repository settings (public/private status, description, etc.).

## Target Audience
- Developers and organizations who need to back up or mirror their GitHub repositories.
- Users requiring a simple GUI or CLI interface for backup operations.

## Key Decisions
- Use Python 3.8 or higher as the development environment.
- Adopt a modular architecture to enhance maintainability.
- Implement a layered architecture to separate concerns.
- Validate tokens comprehensively for security.
- Implement GUI with modular sections for better maintainability.
- Add option to limit the number of repositories to backup.

## Project Structure
- `backup_logic/`: Contains the core logic for backup operations.
- `gui_components.py`: Main GUI component, orchestrating GUI sections.
- `token_section.py`: Module for token input section.
- `backup_section.py`: Module for backup directory section.
- `options_section.py`: Module for backup options section (including repo limit).
- `status_section.py`: Module for status display section.
- `control_section.py`: Module for control buttons section.
- `scripts/`: Includes utility scripts such as token validation and testing.
- `tests/`: Houses unit and integration tests.
- `docs/`: Contains project documentation.

## Usage
- GUI and CLI modes are available for ease of use.
- Detailed logging and error handling are implemented for troubleshooting.

## Security
- Token validation checks for format and permissions.
- Specific scopes are verified.
- Safe subprocess handling and atomic file operations are ensured.
- Logs are sanitized for security.
