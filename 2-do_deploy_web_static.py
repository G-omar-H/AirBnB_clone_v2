#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers,"""
from fabric.api import env, put, run
import os

env.hosts = ['100.25.15.47', ' 	52.91.121.153']


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension> on the web server
        filename = os.path.basename(archive_path)
        folder_name = '/data/web_static/releases/' + os.path.splitext(filename)[0]
        run('mkdir -p {}'.format(folder_name))
        run('tar -xzf /tmp/{} -C {}'.format(filename, folder_name))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current on the web server, linked to the new version of your code
        run('ln -s {} /data/web_static/current'.format(folder_name))

        return True
    except:
        return False
