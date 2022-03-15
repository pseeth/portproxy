"""A command line utility for converting a link (e.g. a Jupyter remote host), replacing the 
localhost:port/rest_of_link with localhost:portproxy_port/rest_of_link.
"""

import shlex
import argbind
from urllib.parse import urlparse
from .portproxy import Args
import subprocess

def open_link(
    machine_name: str,
    url: str,
):
    arg = Args()
    parsed = urlparse(url, allow_fragments=False)
    remote_host, remote_port = parsed.netloc.split(":")

    url = url.replace(remote_host, arg.host)
    url = url.replace(remote_port, f"{arg.port}/{machine_name}/{remote_port}")
    print("\nPortProxy URL")
    print("=============\n")
    print(url)
    print("\n=============")

    try:
        command = f"open {url}"
        subprocess.check_call(shlex.split(command))
    except:
        pass

def forward():
    run = argbind.bind(open_link, positional=True, without_prefix=True)
    args = argbind.parse_args()
    with argbind.scope(args):
        run()
