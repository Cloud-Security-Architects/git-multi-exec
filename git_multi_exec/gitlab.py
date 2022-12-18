import logging

import gitlab

from .util import RemoteCallback, clone_and_run

log = logging.getLogger(__name__)


class Runner:
    def __init__(self, token, command):
        self.command = command
        self.gl = gitlab.Gitlab(private_token=token)
        self.callback = RemoteCallback("", token)

    def scan_all(self):
        for group in self.gl.groups.list():
            self.scan_group(group)

    def scan_group(self, group):
        try:
            for project in group.projects.list():
                clone_and_run(
                    project.http_url_to_repo,
                    command=self.command,
                    callback=self.callback,
                )
            for subgroup in group.descendant_groups.list():
                log.debug("Descending into subgroup: %s", subgroup)
                self.scan_group(subgroup)
        except gitlab.exceptions.GitlabListError:
            log.error("Failed to list '%s' contents, check permissions", group)
