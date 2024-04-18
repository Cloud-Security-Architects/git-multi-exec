[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

:warning: **Do not use with untrusted user input. This script will execute shell commands in your environment.** :warning:

# git-multi-exec

`git-multi-exec` is a tool to run a command in a local clone of a git repository.

By default it will run `spectral scan --include-tags base,audit,iac` against each repo.

The repositories are collected recursively from the top, based on available permissions.

# Installation
`pip install git+https://github.com/Cloud-Security-Architects/git-multi-exec`

# Usage
1. Configure credentials for your Git SaaS platforms as environment variables.

    ```env
    BITBUCKET_USER=
    BITBUCKET_PAT=

    GITLAB_PAT=

    GITHUB_PAT=

    AZURE_DEVOPS_PAT=
    ```

2. Run `git-multi-exec <platform>` with platform being one of `github`, `gitlab`, `bitbucket` or `azure-devops`.
   By default it will run `spectral scan --include-tags base,audit,iac`.

   Azure DevOps supports specifying an organization with `--org <organization_name>` and ignoring specific organizations in regular mode with `--ignore-accounts account1,account2,...`. 


# Required permissions

## Audit
### GitHub
#### Classic
- repo
- read:org
- read:user
#### Fine-grained (beta)
TODO

### GitLab
- read_api
- read_user
- read_repository

### BitBucket
- Account
    - Read
- Workspace membership
    - Read
- Projects
    - Read
- Repositories
    - Read

### Azure DevOps
#### Single org
- Code
    - Read
- Project / Team
    - Read
#### All orgs
- Identity
 - Read
- Code
  - Read
- Project / Team
  - Read

# Structure
How `git-multi-exec` handles each platform

## For GitHub
Collects all organizations and descends into their repositories.

## For GitLab
Collects all groups and descends into repositories.
Subgroups are listed by the API as part of all groups.

## For BitBucket
Collects all workspaces and descends into projects and repositories.

## For Azure DevOps
Collects all projects under an organization and iterates over their repositories.