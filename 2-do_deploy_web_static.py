#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import task, env, put, run, local
import os
from datetime import datetime

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
    """
    distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        filename = os.path.basename(archive_path)
        foldername = filename.split('.')[0]
        run('rm -rf /data/web_static/releases/{}/'.format(foldername))
        run('mkdir -p /data/web_static/releases/{}'.format(foldername))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(filename, foldername))
  
        run('rm /tmp/{}'.format(filename))
        run('rm -rf /data/web_static/releases/\
            {}/web_static/*'.format(foldername))
        run('rm -rf /data/web_static/current')

        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(foldername))

        print("New version deployed!")
        return True
    except Exception:
        return False
