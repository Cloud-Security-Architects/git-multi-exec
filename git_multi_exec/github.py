import logging

from octokit import Octokit

from .util import RemoteCallback, clone_and_run

log = logging.getLogger(__name__)


class Runner:
    def __init__(self, token, command):
        self.command = command
        self.gh = Octokit(auth="token", token=token)
        self.callback = RemoteCallback("x-access-token", token)

    def scan_all(self):
        orgs = [org["login"] for org in self.gh.orgs.list_for_authenticated_user().json]
        for org in orgs:
            repos = self.gh.repos.list_organization_repositories(org=org).json
            for repo in repos:
                clone_and_run(
                    repo["clone_url"], command=self.command, callback=self.callback
                )
