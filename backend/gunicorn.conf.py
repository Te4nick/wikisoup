from os import getenv

bind = f'{getenv(key="HOST", default="127.0.0.1")}:{getenv(key="PORT", default=8000)}'
wsgi_app = 'wikisoup.wsgi:application'
workers = getenv(key='WORKERS', default=2)
threads = getenv(key='THREADS', default=4)
