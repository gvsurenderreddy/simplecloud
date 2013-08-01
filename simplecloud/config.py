# -*- coding: utf-8 -*-

import os

from utils import (make_dir, INSTANCE_FOLDER_PATH, SHARED_STORAGE_PATH,
        IMAGE_POOL_PATH, VM_POOL_PATH, INSTANCE_CONFIG_PATH, copy_file)


class BaseConfig(object):

    PROJECT = "simplecloud"

    # Get app root path, also can use flask.root_path.
    # ../../config.py
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    ADMINS = ['simplecloud@qq.com']

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = 'secret key'

    make_dir(INSTANCE_CONFIG_PATH)
    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')
    make_dir(LOG_FOLDER)
    
    # Create image pool and vm pool
    make_dir(SHARED_STORAGE_PATH)
    make_dir(IMAGE_POOL_PATH)
    make_dir(VM_POOL_PATH)


class DefaultConfig(BaseConfig):

    DEBUG = True

    # Flask-Sqlalchemy: http://packages.python.org/Flask-SQLAlchemy/config.html
    SQLALCHEMY_ECHO = True
    # SQLITE for prototyping.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + INSTANCE_FOLDER_PATH + '/db.sqlite'
    # MYSQL for production.
    #SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db?charset=utf8'

    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = ['zh_CN', 'en']
    BABEL_DEFAULT_LOCALE = 'en'
    LOCALE_SETTING = "zh_CN"

    # Flask-cache: http://pythonhosted.org/Flask-Cache/
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60

class TestConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
