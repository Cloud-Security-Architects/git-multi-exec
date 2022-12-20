import logging

import gitlab

from .util import RemoteCallback, clone_and_run

log = logging.getLogger(__name__)


class Runner:
    def __init__(self, token, command, url=None):
        self.command = command
        self.gl = gitlab.Gitlab(private_token=token, url=url)
        self.callback = RemoteCallback("", token)

    def scan_all(self):
        for group in self.gl.groups.list():
            log.debug("About to scan group '%s'", group.name)
            self.scan_group(group)

    def scan_group(self, group):
        log.debug("Entering group '%s'", group.name)
        try:
            for project in group.projects.list():
                log.debug("Scanning '%s'", project.name)
                clone_and_run(
                    project.http_url_to_repo,
                    command=self.command,
                    callback=self.callback,
                )
        except gitlab.exceptions.GitlabListError:
            log.error("Failed to list '%s' contents, check permissions", group)
