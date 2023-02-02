import logging

import atlassian.bitbucket

from .util import RemoteCallback, clone_and_run

log = logging.getLogger(__name__)


class Runner:
    def __init__(self, auth, command, url=None):
        self.command = command
        username, password = auth
        self.bitbucket = atlassian.bitbucket.Cloud(
            username=username, password=password, cloud=True
        )
        self.callback = RemoteCallback(username, password)

    def scan_workspace(self, workspace):
        for project in workspace.projects.each():
            for repo in project.repositories.each():
                clone_link = repo.get_clone_link()
                clone_and_run(clone_link, command=self.command, callback=self.callback)

    def get_workspace(self, workspace_name):
        return self.bitbucket.workspaces.get(workspace_name)

    def scan_all(self):
        for workspace in self.bitbucket.workspaces.each():
            self.scan_workspace(workspace)


class DatacenterRunner:
    def __init__(self, auth, command, url):
        self.command = command
        username, password = auth
        self.bitbucket = atlassian.bitbucket.Bitbucket(
            url=url, username=username, password=password
        )
        self.callback = RemoteCallback(username, password)

    def scan_all(self):
        for project in self.bitbucket.project_list():
            for repo in self.bitbucket.repo_list(project["key"]):
                clone_link = [
                    x["href"] for x in repo["links"]["clone"] if x["name"] == "http"
                ][0]
                clone_and_run(clone_link, command=self.command, callback=self.callback)


# The package doesn't have a simple way to get the clone link otherwise.
def get_clone_link(self, protocol="https"):
    """
    Get a clone link.
    """
    links = self.get_data("links")
    if links is None:
        return None
    return [x["href"] for x in links["clone"] if x["name"] == protocol][0]


atlassian.bitbucket.cloud.repositories.Repository.get_clone_link = get_clone_link
