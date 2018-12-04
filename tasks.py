# -*- coding: utf-8 -*-

import os
import shutil
import sys
from datetime import datetime
try:
    import socketserver
except ImportError:
    import SocketServer as socketserver

from invoke import task
from invoke.util import cd
from pelican.server import ComplexHTTPRequestHandler

CONFIG = {
    'content_path': 'content',
    # Local path configuration (can be absolute or relative to tasks.py)
    'deploy_path': 'output',
    # Github Pages configuration
    'github_pages_branch': 'gh-pages',
    'commit_message': "'Publish site on {:%Y-%m-%d %H:%M}'".format(datetime.now()),
    # Port for `serve`
    'port': 8000,
}

META = """Title:
Date: {:%Y-%m-%d %H:%M}
Category: 机器学习,金融与算法,玩电脑,杂记
Tags:
Slug:
Authors: Kevin Chen
Status: draft
"""

@task
def clean(c):
    """Remove generated files"""
    if os.path.isdir(CONFIG['deploy_path']):
        shutil.rmtree(CONFIG['deploy_path'])
        os.makedirs(CONFIG['deploy_path'])

@task
def build(c):
    """Build local version of site"""
    c.run('pelican -s pelicanconf.py')

@task
def rebuild(c):
    """`build` with the delete switch"""
    c.run('pelican -d -s pelicanconf.py')

# @task
# def regenerate(c):
#     """Automatically regenerate site upon file modification"""
#     c.run('pelican -r -s pelicanconf.py')

@task
def serve(c):
    """Serve site at http://localhost:8000/"""
    os.chdir(CONFIG['deploy_path'])

    class AddressReuseTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        ('', CONFIG['port']),
        ComplexHTTPRequestHandler)

    sys.stderr.write('Serving on port {port} ...\n'.format(**CONFIG))
    server.serve_forever()

@task
def reserve(c):
    """`build`, then `serve`"""
    build(c)
    serve(c)

@task
def preview(c):
    """Build production version of site"""
    c.run('pelican -s publishconf.py')


@task
def publish(c):
    """Publish to production via rsync"""
    c.run('pelican -s publishconf.py')
    c.run(
        'rsync --delete --exclude ".DS_Store" -pthrvz -c '
        '{} {production}:{dest_path}'.format(
            CONFIG['deploy_path'].rstrip('/') + '/',
            **CONFIG))

@task
def gh_pages(c):
    """Publish to GitHub Pages"""
    preview(c)
    c.run('ghp-import -b {github_pages_branch} '
          '-m {commit_message} '
          '{deploy_path} -p'.format(**CONFIG))
    

@task
def preview(c):
    """Build production version of site"""
    c.run('pelican -d -s pelicanconf.py -t themes/plumage')
    os.chdir(CONFIG['deploy_path'])
    print("Server at http://127.0.0.1:8000")
    c.run('python -m http.server 8000 -b 127.0.0.1')

@task
def github(c):
    """Build production version of site"""
    c.run('pelican -d -s publishconf.py -t themes/plumage')
    c.run('git add --all')
    c.run('git commit -m {}'.format(CONFIG['commit_message']))
    c.run('git push origin master')

@task
def new(c):
    """Build production version of site"""
    os.chdir(CONFIG['content_path'])
    with open('new.md', 'w') as f:
        f.write(META.format(datetime.now()))

