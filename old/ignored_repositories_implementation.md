# Ignoring Repositories during Backup

This document explains how to configure the GitHub Backup tool to ignore specific repositories during the backup process. This feature is useful when you have certain repositories that you do not want to include in your backups.

## How to Ignore Repositories

To ignore repositories, you need to create a file named `ignored_repos.txt` in the root directory of the GitHub Backup project (the same directory where `github_backup.py` is located).

In this `ignored_repos.txt` file, list the names of the repositories you want to ignore, with one repository name per line.

**Example `ignored_repos.txt`:**

```
repo-to-ignore-1
another-repo-to-ignore
example-repo
```

In this example, the repositories named `repo-to-ignore-1`, `another-repo-to-ignore`, and `example-repo` will be ignored during the backup process.

**Important Notes:**

-   **Repository Name Only:**  Only include the repository name (e.g., `my-repo`) in the `ignored_repos.txt` file, not the full repository name with the owner (e.g., `owner/my-repo`).
-   **Case-Sensitive:** Repository names are case-sensitive. Ensure the names in `ignored_repos.txt` exactly match the repository names as they appear on GitHub.
-   **File Location:** The `ignored_repos.txt` file must be placed in the root directory of the GitHub Backup project for the tool to recognize it.
-   **Empty File:** If the `ignored_repos.txt` file is empty or does not exist, no repositories will be ignored.

By following these steps, you can easily exclude specific repositories from your GitHub backups.