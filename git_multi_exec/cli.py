import logging
import os
import shlex

import click
from dotenv import load_dotenv

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

load_dotenv()

from . import bitbucket, github, gitlab


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
def do_github(command):
    click.secho("🔰 Starting GitHub scan", fg="green")
    scanner = github.Runner(os.environ["GITHUB_PAT"], command)
    scanner.scan_all()
