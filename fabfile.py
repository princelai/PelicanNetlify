import os
from datetime import datetime

from fabric.api import env, local

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
env.content_path = 'content'


META = """Title:
Date: {:%Y-%m-%d %H:%M}
Category: IT笔记, 金融笔记
Tags:
Slug:
Authors: Kevin Chen
Status: draft
"""


def new():
    os.chdir(env.content_path)
    with open('new.md', 'w') as f:
        f.write(META.format(datetime.now()))

def preview():
    local('pelican -d -s pelicanconf.py')
    os.chdir(env.deploy_path)
    local('python -m http.server 8000 -b 127.0.0.1')


def github():
    local('git add --all')
    local('git commit -m "update at {:%Y-%m-%d %H:%M}"'.format(datetime.now()))
    local('git push origin master')
