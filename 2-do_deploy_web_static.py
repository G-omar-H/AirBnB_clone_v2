#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import env, put, run
import os

env.hosts = ['100.25.15.47', ' 	52.91.121.153']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        filename = os.path.basename(archive_path)
        folder_name = '/data/web_static/releases/' +\
            os.path.splitext(filename)[0]
        run('mkdir -p {}'.format(folder_name))
        run('tar -xzf /tmp/{} -C {}'.format(filename, folder_name))

        run('rm /tmp/{}'.format(filename))

        run('rm -rf /data/web_static/current')

        run('ln -s {} /data/web_static/current'.format(folder_name))

        return True
    except Exception:
        return False
