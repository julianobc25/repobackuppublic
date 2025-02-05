# GitHub Token Generation Guide

Since the current tokens are being rejected by GitHub, you'll need to generate new tokens. Here's how:

## For Source Token

1. Go to GitHub.com and sign in with your source account
2. Click your profile picture > Settings
3. Scroll down to "Developer settings" (bottom of left sidebar)
4. Click "Personal access tokens" > "Fine-grained tokens"
5. Click "Generate new token"
6. Set the following:
   - Token name: "GitHub Backup Tool - Source"
   - Expiration: Choose an appropriate duration
   - Repository access: "All repositories"
   - Permissions:
     - Repository: "Read" access for "Contents", "Metadata"
     - Organization: "Read" access for "Members"

## For Destination Token

1. Go to GitHub.com and sign in with your destination account
2. Follow the same steps to get to token generation
3. Set the following:
   - Token name: "GitHub Backup Tool - Destination"
   - Expiration: Choose an appropriate duration
   - Repository access: "All repositories"
   - Permissions:
     - Repository: "Read and Write" access for "Contents", "Metadata"
     - Repository: "Delete" access for "Administration"
     - Organization: "Read" access for "Members"

## After Generating Tokens

1. Copy each token immediately after generation
2. Update your .env file with the new tokens:
   ```
   SOURCE_GITHUB_TOKEN=ghp_your_new_source_token_here
   DEST_GITHUB_TOKEN=ghp_your_new_dest_token_here
   ```
3. Save the .env file and try running the backup tool again

**Important Notes:**
- Save your tokens securely - they can't be viewed again after generation
- Make sure to note the expiration date you set
- Double-check that all required permissions are enabled