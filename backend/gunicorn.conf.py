from os import getenv

bind = '0.0.0.0:8000'
wsgi_app = 'wikisoup.wsgi:application'
workers = 4
threads = 2
