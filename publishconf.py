#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

SITEURL = 'https://www.solarck.com'
MIXCONTENT = '//www.solarck.com'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
# CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = 'solarck'
GOOGLE_ANALYTICS = 'UA-1337838-7'
