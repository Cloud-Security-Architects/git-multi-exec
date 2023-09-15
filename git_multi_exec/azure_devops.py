import logging

import click

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

from .util import RemoteCallback, clone_and_run


log = logging.getLogger(__name__)


class Runner:
    def __init__(self, token, command):
        self.command = command
        self.token = token
        self.credentials = BasicAuthentication("", token)
        self.url = "https://app.vssps.visualstudio.com/"
        self.connection = Connection(base_url=self.url, creds=self.credentials)

    def scan_all(self):
        accounts_client = self.connection.clients.get_accounts_client()
        member_id = self.connection.clients.get_identity_client().get_self().id

        accounts = accounts_client.get_accounts(member_id=member_id)
        click.secho(
            f"Found {len(accounts)} organizations: {', '.join(k.account_name for k in accounts)}"
        )

        for account in accounts:
            click.secho(f"Processing {account.account_name}...")
            account_runner = OrgRunner(
                token=self.token, command=self.command, org=account.account_name
            )
            account_runner.scan_all()


class OrgRunner:
    def __init__(self, token, command, org=None):
        self.command = command
        self.credentials = BasicAuthentication("", token)
        if org:
            self.url = f"https://dev.azure.com/{org}"

        self.connection = Connection(base_url=self.url, creds=self.credentials)
        self.callback = RemoteCallback(org, token)

    def scan_all(self):
        client = self.connection.clients.get_core_client()
        git_client = self.connection.clients.get_git_client()

        projects = client.get_projects()
        click.secho(
            f"Found {len(projects)} projects: {', '.join(k.name for k in projects)} "
        )

        for project in projects:
            click.secho(f"Collecting repos for {project.name}")
            repos = git_client.get_repositories(project.id)
            click.secho(f"Found {len(repos)} repositories.")
            for repo in repos:
                clone_and_run(repo.remote_url, self.command, self.callback)
