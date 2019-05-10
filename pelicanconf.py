#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Kevin Chen'
SITENAME = 'Solarck'

SITEDESCRIPTION = '金融民工与程序猿的结合体'
SITESUBTITLE = '金融民工与程序猿的结合体'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh-cn'
DATE_FORMATS = {
    'zh-cn': '%B %d, %Y',
}

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Plugin
PLUGIN_PATHS = ["plugins", "./plugins"]
PLUGINS = [
    "render_math", "tag_cloud", "tipue_search", "pelican-toc", "neighbors",
    "related_posts"
]
TYPOGRIFY = True


# MENU
# MENUITEMS = (('关于','about'),
# ('简历','resume'))

# TOC
TOC = {
    'TOC_HEADERS': '^h[1-4]',  # What headers should be included in
    # the generated toc
    # Expected format is a regular expression
    'TOC_RUN': 'true',  # Default value for toc generation,
    # if it does not evaluate
    # to 'true' no toc will be generated
    'TOC_INCLUDE_TITLE': 'false',  # If 'true' include title in toc
}

# Blogroll
LINKS_WIDGET_NAME = '链接'
LINKS = (
    ('Pelican', 'http://getpelican.com/'),
)

# Social widget
# SOCIAL = (('Github', 'https://github.com/princelai'),
#          ('G+', 'https://plus.google.com/100073068742779779797'),
#          ('Twitter','https://twitter.com/princelai'))

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing

ROBOTS_SAVE_AS = 'robots.txt'
SITEMAP_SAVE_AS = 'sitemap.xml'
DATE_FORMATS = {
    'zh': '%B %d, %Y',
}

# EXTRA_PATH_METADATA = {
#     'extra/robots.txt': {'path': 'robots.txt'},
#     'extra/favicon.ico': {'path': '/static/favicon.ico'}
# }

STATIC_PATHS = ['_redirects', 'favicon.ico', 'CNAME', 'static']

# THEME
# THEME = 'pelicanyan'
# DIRECT_TEMPLATES = ('index', 'categories', 'authors', 'archives', 'sitemap', 'robots')

THEME = 'plumage'
TIPUE_SEARCH = True
ARCHIVES_SAVE_AS = 'archives.html'
CATEGORIES_SAVE_AS = 'categories.html'
TAGS_SAVE_AS = 'tags.html'
SITE_THUMBNAIL = 'static/avatar.jpg'
DIRECT_TEMPLATES = ('index', 'categories', 'authors', 'archives', 'search')

# THEME = 'notmyidea'
#SOCIAL_WIDGET_NAME = '社交网站'
#GOOGLE_ANALYTICS = 'UA-1337838-7'

# THEME = 'blueidea'

#THEME = 'gum'
#GOOGLE_ANALYTICS_ID = 'UA-1337838-7'
#GOOGLE_ANALYTICS_SITENAME = 'Solarck'
#GITHUB_URL = 'https://github.com/princelai'
#TWITTER_URL = 'https://twitter.com/princelai'
#GOOGLEPLUS_URL = 'https://plus.google.com/100073068742779779797'
