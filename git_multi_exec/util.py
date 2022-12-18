import subprocess
import tempfile
import logging

import click
import pygit2

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)


class RemoteCallback(pygit2.RemoteCallbacks):
    def __init__(self, user, token):
        self.user = user
        self.token = token

    def credentials(self, url, username_from_url, allowed_types):
        return pygit2.UserPass(self.user, self.token)


def clone_and_run(clone_link: str, command, callback=None) -> None:
    with tempfile.TemporaryDirectory() as tempdir:
        click.secho(f"💫 Cloning '{clone_link}' into: {tempdir}", fg="blue")
        pygit2.clone_repository(clone_link, tempdir, callbacks=callback)
        click.secho("💻 Executing command...", fg="blue")
        spectral = subprocess.Popen(
            command, cwd=tempdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = spectral.communicate()
        print(out.decode())
        print(err.decode())
