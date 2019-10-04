# -*- coding: utf-8 -*-

import os
import shutil
import sys
from datetime import datetime

from invoke import task
from invoke.util import cd


CONFIG = {
    'content_path': 'content',
    'deploy_path': 'output',
    'commit_message': "'Publish site on {:%Y-%m-%d %H:%M}'".format(datetime.now()),
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

@task
def updateenv(c):
    """update netlify's pelican envirement"""
    c.run('pip freeze > requirements.txt')
    c.run("python --version|cut -d ' ' -f 2|cut -c1-3 > runtime.txt")
