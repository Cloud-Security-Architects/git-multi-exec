import logging

from github import Github

from .util import RemoteCallback, clone_and_run

log = logging.getLogger(__name__)


class Runner:
    def __init__(self, token, command, url=None):
        self.command = command
        if url:
            self.gh = Github(login_or_token=token, base_url=url)
        else:
            self.gh = Github(login_or_token=token)
        self.callback = RemoteCallback("x-access-token", token)

    def scan_all(self):
        # Get the orgs for the currently authenticated user
        orgs = self.gh.get_user().get_orgs()
        for org in orgs:
            log.debug("Scanning org %s", org.login)
            repos = org.get_repos('member')
            for repo in repos:
                clone_and_run(
                    repo.clone_url, command=self.command, callback=self.callback
                )
