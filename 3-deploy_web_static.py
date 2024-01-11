#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers,
"""

from fabric.api import env


env.user = 'ubuntu'
env.hosts = ['100.25.15.47', '52.91.121.153']


def deploy():
    """
    creates and distributes an archive to your web server
    """
    try:
        archive_path = do_pack()
        return do_deploy(archive_path)
    except Exception:
        return False
