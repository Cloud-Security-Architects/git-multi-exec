import logging

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

from .util import RemoteCallback, clone_and_run


log = logging.getLogger(__name__)


class Runner:
    def __init__(self, token, command, org=None):
        self.command = command
        self.credentials = BasicAuthentication("", token)
        self.url = f"https://dev.azure.com/{org}"
        self.connection = Connection(base_url=self.url, creds=self.credentials)
        self.callback = RemoteCallback(org, token)

    def scan_all(self):
        client = self.connection.clients.get_core_client()
        git_client = self.connection.clients.get_git_client()

        get_projects_response = client.get_projects()

        for project in get_projects_response:
            print(f"Collecting repos for {project.name}")
            repos = git_client.get_repositories(project.id)
            print(repos)
            for repo in repos:
                clone_and_run(repo.remote_url, self.command, self.callback)
