#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the contents of the
    web_static folder of your AirBnB Clone repo, using the function do_pack.
"""

from fabric.api import local, task
from datetime import datetime


@task
def do_pack():
    """
    pack .tgz archive from web_static folder
    """
    try:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(current_time)
        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None
