#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers,
"""

from fabric.api import env,  task, put, run, local
from datetime import datetime
import os

env.hosts = ['100.25.15.47', '52.91.121.153']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


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

@task
def do_deploy(archive_path):
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


@task
def deploy():
    """
    creates and distributes an archive to your web server
    """
    try:
        archive_path = do_pack()
        return do_deploy(archive_path)
    except Exception:
        return False
