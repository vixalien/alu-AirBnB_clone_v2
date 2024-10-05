#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import run, put, env
from os import path

env.hosts = ['54.152.219.25', '3.83.237.118']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/keys/intranet'


def do_deploy(archive_path):
    """Deploy web files to server"""
    try:
        if not path.exists(archive_path):
            return False

        # Upload archive
        put(archive_path, '/tmp/')

        # Create target dir
        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'
            .format(timestamp))

        # Uncompress archive and delete .tgz
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C '
            '/data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # Remove archive
        run('sudo rm /tmp/web_static_{}.tgz'
            .format(timestamp))

        # Move contents into host web_static
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* '
            '/data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # Remove extraneous web_static dir
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'
            .format(timestamp))

        # Delete pre-existing sym link
        run('sudo rm -rf /data/web_static/current')

        # Re-establish symbolic link
        run('sudo ln -s /data/web_static/releases/web_static_{}/ '
            '/data/web_static/current'
            .format(timestamp))
    except Exception as e:
        print("Exception:", e)
        return False

    # Return True on success
    return True
