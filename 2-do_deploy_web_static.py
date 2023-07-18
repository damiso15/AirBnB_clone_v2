#!/usr/bin/python3
"""
Fabric script for deploying an archive to web servers
"""


from fabric.api import env, put, run
import os


env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with actual IP addresses
env.user = 'ubuntu'  # Replace with actual username
env.key_filename = '/path/to/your/ssh/private/key'  # Replace with actual SSH key path


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        archive_folder = '/data/web_static/releases/' + archive_filename[:-4]
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(archive_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, archive_folder))
        run('rm /tmp/{}'.format(archive_filename))
        run('mv {}/web_static/* {}'.format(archive_folder, archive_folder))
        run('rm -rf {}/web_static'.format(archive_folder))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(archive_folder))
        print('New version deployed!')
        return True
    except Exception as e:
        print('Deployment failed:', str(e))
        return False
