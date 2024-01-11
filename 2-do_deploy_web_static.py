#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers,
    using the function do_deploy.
"""

from socket import AI_NUMERICHOST
from fabric.api import *
from os.path import exists
env.hosts = ['421116-web-01', '421116-web-02']
env.user = "ubuntu"


def do_deploy(archive_path):
    """
    deploy archive to web servers
    """
    if exists(archive_path) is False:
        return False
    try:
        archive = archive_path.split("/")[-1]
        archive_name = archive.split(",")[0]
        put(archive_path, "/tmp/{}".format(archive))
        run('mkdir -p "/data/web_static/releases/{}".format(archive_name)')
        run("tar -xzf /tmp/{} -C /data/web_statis/releases/{}"
            .format(archive, archive_name))
        run("rm /tmp/{}".format(archive))
        run("rm /data/web_static/current")
        run("ln -s /data/web_static/releases/{}\
            /data/web_static/current".format(archive_name))
        return True
    except Exception:
        return False
