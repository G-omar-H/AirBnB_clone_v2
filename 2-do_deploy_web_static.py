#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import env, put, run
import os
from datetime import datetime

env.hosts = ['100.25.15.47', '52.91.121.153']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
    distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        filename = os.path.basename(archive_path)
        foldername = filename.split('.')[0]
        run('mkdir -p /data/web_static/releases/{}'.format(foldername))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(filename, foldername))
        run('rm /tmp/{}'.format(filename))

        run('rm -rf /data/web_static/current')

        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(foldername))

        return True
    except Exception:
        return False
