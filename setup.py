# -*- coding: utf-8 -*-

from setuptools import setup

project = "simplecloud"

setup(
    name=project,
    version='0.1',
    url='https://github.com/simplecloud/simplecloud',
    description='SimpleCloud is an IaaS(Infrastructure as a Service) software.',
    author='SimpleCloud',
    author_email='simplecloud@qq.com',
    packages=["simplecloud"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'Flask-Script',
        'Flask-Babel',
        'Flask-Testing',
        'Flask-Mail',
        'Flask-Cache',
        'Flask-Login',
        'Flask-OpenID',
        'nose',
        'mysql-python',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries'
    ]
)
