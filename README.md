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
```

2. Run `git-multi-exec`


# Structure
How `git-multi-exec` handles each platform under `scan_all`:

## For GitHub
Collects all organizations and descends into their repositories.

## For GitLab
Collects all groups and descends into subgroups and repositories.

## For BitBucket
Collects all workspaces and descends into projects and repositories.


