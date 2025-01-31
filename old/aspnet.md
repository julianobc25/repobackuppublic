# Building a Website to Mirror/Clone a GitHub Repository

## Step-by-Step Guide

### 1. Set Up Your Development Environment
Before you start coding, ensure your development environment is ready:

- Install Visual Studio (Community Edition is free) or Visual Studio Code.
- Install the .NET SDK (latest version).
- Create a GitHub account if you don’t already have one.
- Generate a Personal Access Token (PAT) from GitHub for API access:
  - Go to [GitHub Developer Settings](https://github.com/settings/tokens).
  - Generate a token with permissions like `repo` (for private repositories) and `public_repo` (for public repositories).

### 2. Create a New ASP.NET Core Project
Open a terminal or command prompt and run the following commands:

```bash
dotnet new webapp -n GitHubMirrorTool
cd GitHubMirrorTool
```

Open the project in Visual Studio or Visual Studio Code.

### 3. Add Required NuGet Packages
Install the Octokit library to interact with the GitHub API:

```bash
dotnet add package Octokit
```

### 4. Configure GitHub API Access
Open the `appsettings.json` file in your project and add your GitHub credentials:

```json
{
  "GitHub": {
    "AccessToken": "your_personal_access_token_here"
  }
}
```

In the `Program.cs` file, configure the app to read these settings:

```csharp
var builder = WebApplication.CreateBuilder(args);

// Add configuration
builder.Services.Configure<GithubSettings>(builder.Configuration.GetSection("GitHub"));

// Other configurations...
```

Create a `GithubSettings` class to hold the configuration:

```csharp
public class GithubSettings
{
    public string AccessToken { get; set; }
}
```

### 5. Create a Service to Interact with GitHub
Create a folder called `Services` in your project and add a new file `GitHubService.cs`:

```csharp
using Octokit;
using System.Threading.Tasks;

public class GitHubService
{
    private readonly GitHubClient _gitHubClient;

    public GitHubService(GithubSettings settings)
    {
        _gitHubClient = new GitHubClient(new ProductHeaderValue("GitHubMirrorTool"));
        _gitHubClient.Credentials = new Credentials(settings.AccessToken);
    }

    public async Task<Repository> CloneRepositoryAsync(string sourceOwner, string sourceRepo, string targetOwner, string targetRepo)
    {
        // Fetch the source repository
        var sourceRepository = await _gitHubClient.Repository.Get(sourceOwner, sourceRepo);

        // Create a new repository in the target account
        var newRepository = new NewRepository(targetRepo)
        {
            Description = sourceRepository.Description,
            Private = sourceRepository.Private
        };

        var createdRepository = await _gitHubClient.Repository.Create(targetOwner, newRepository);

        // Mirror the repository contents
        // This is a basic example. For comprehensive mirroring, consider using Git commands (e.g., git clone --mirror) or additional GitHub API calls.

        return createdRepository;
    }
}
```

Register the service in `Program.cs`:

```csharp
builder.Services.AddSingleton<GitHubService>();
```

### 6. Create a Controller for the API
Create a folder called `Controllers` in your project and add a new file `GitHubController.cs`:

```csharp
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

[ApiController]
[Route("api/[controller]")]
public class GitHubController : ControllerBase
{
    private readonly GitHubService _gitHubService;

    public GitHubController(GitHubService gitHubService)
    {
        _gitHubService = gitHubService;
    }

    [HttpPost("clone")]
    public async Task<IActionResult> CloneRepository([FromBody] CloneRequest request)
    {
        try
        {
            var result = await _gitHubService.CloneRepositoryAsync(
                request.SourceOwner,
                request.SourceRepo,
                request.TargetOwner,
                request.TargetRepo
            );

            return Ok(new { Message = "Repository cloned successfully!", Repository = result });
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { Error = ex.Message });
        }
    }
}

public class CloneRequest
{
    public string SourceOwner { get; set; }
    public string SourceRepo { get; set; }
    public string TargetOwner { get; set; }
    public string TargetRepo { get; set; }
}
```

### 7. Create a Frontend Interface
Use Razor Pages or a JavaScript framework like React to build a simple UI. Here is an example using Razor Pages:

**Pages/Index.cshtml:**
```html
@page
@model IndexModel
@{
    ViewData["Title"] = "GitHub Mirror Tool";
}

<h1>Clone a GitHub Repository</h1>
<form id="cloneForm">
    <label for="sourceOwner">Source Owner:</label>
    <input type="text" id="sourceOwner" name="sourceOwner" required />

    <label for="sourceRepo">Source Repository:</label>
    <input type="text" id="sourceRepo" name="sourceRepo" required />

    <label for="targetOwner">Target Owner:</label>
    <input type="text" id="targetOwner" name="targetOwner" required />

    <label for="targetRepo">Target Repository:</label>
    <input type="text" id="targetRepo" name="targetRepo" required />

    <button type="submit">Clone Repository</button>
</form>

<script>
    document.getElementById('cloneForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);

        try {
            const response = await fetch('/api/github/clone', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sourceOwner: formData.get('sourceOwner'),
                    sourceRepo: formData.get('sourceRepo'),
                    targetOwner: formData.get('targetOwner'),
                    targetRepo: formData.get('targetRepo')
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status} - ${response.statusText}`);
            }

            const result = await response.json();
            alert(result.Message || result.Error);
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    });
</script>
```

### 8. Test and Run the Application
Run the application:

```bash
dotnet run
```

Open your browser and navigate to `https://localhost:5001`. Test the form by entering valid GitHub repository details.

### 9. Deploy the Application
Once your application is working locally, you can deploy it to platforms like:
- Azure App Service
- Heroku
- AWS Elastic Beanstalk

### Next Steps
Enhance the tool to handle more complex scenarios (e.g., mirroring branches, pull requests, issues).
- Add authentication to restrict access to the tool.
- Use Git commands (via `System.Diagnostics.Process`) to perform deeper cloning/mirroring.

This project will give you hands-on experience with C#, ASP.NET Core, and the GitHub API. Let me know if you need further clarification or help!
