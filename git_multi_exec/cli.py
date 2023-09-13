import logging
import os
import shlex

import click
from dotenv import load_dotenv

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

load_dotenv()

from . import bitbucket, github, gitlab, azure_devops


@click.group()
def cli():
    # No generic actions
    pass


@cli.command("gitlab")
@click.option(
    "--command", type=shlex.split, default="spectral scan --include-tags base,audit,iac"
)
def do_gitlab(command):
    click.secho("🔰 Starting GitLab scan", fg="green")
    scanner = gitlab.Runner(os.environ["GITLAB_PAT"], command, os.environ["GITLAB_URL"])
    scanner.scan_all()


@cli.command("bitbucket")
@click.option(
    "--command", type=shlex.split, default="spectral scan --include-tags base,audit,iac"
)
@click.option("--url", type=str, default=None)
def do_bitbucket(command, url):
    click.secho("🔰 Starting BitBucket scan", fg="green")
    if url:
        scanner = bitbucket.DatacenterRunner(
            (os.environ["BITBUCKET_USER"], os.environ["BITBUCKET_PAT"]),
            command,
            url=url,
        )
    else:
        scanner = bitbucket.Runner(
            (os.environ["BITBUCKET_USER"], os.environ["BITBUCKET_PAT"]),
            command,
            url=url,
        )
    scanner.scan_all()


@cli.command("github")
@click.option(
    "--command", type=shlex.split, default="spectral scan --include-tags base,audit,iac"
)
@click.option("--org")
def do_github(command, org):
    click.secho("🔰 Starting GitHub scan", fg="green")

    scanner = github.Runner(os.environ["GITHUB_PAT"], command)
    if org:
        scanner.scan_org(org)
    else:
        scanner.scan_all()


@cli.command("azure-devops")
@click.option(
    "--command", type=shlex.split, default="spectral scan --include-tags base,audit,iac"
)
@click.option("--org")
def do_azure_devops(command, org):
    click.secho("🔰 Starting Azure DevOps scan", fg="green")

    if org:
        scanner = azure_devops.Runner(os.environ["AZURE_DEVOPS_PAT"], command, org=org)
        scanner.scan_all()
    else:
        click.secho("org is required for ADO")
