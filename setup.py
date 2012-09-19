"""
hipflask
-------------

A container for setting up your basic RESTful single page flask app

Sets up flask-login, flask-sqlalchemy, flask-script, flask-superadmin, and flask-migrate
Provides a basic RESTful api handler for your models

Creates a client environment using boostrap, knockout, jquery

Intended to get you up and running quickly

"""
from setuptools import setup


setup(
    name='hipflask',
    version='0.3.2',
    url='http://github.com/robertfw/hipflask',
    license='License :: OSI Approved :: MIT License',
    author='Robert Warner',
    author_email='radicalphoenix@gmail.com',
    description='Quickstart tool for setting up common flask extensions and tools',
    long_description=__doc__,
    packages=['hipflask'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-Login',
        'Flask-SQLAlchemy',
        'Flask-Script',
        'Flask-SuperAdmin',
        'Flask-WTF',
        'Jinja2',
        'SQLAlchemy',
        'Tempita',
        'WTForms',
        'Werkzeug',
        'argparse',
        'blinker',
        'decorator',
        'passlib',
        'simplejson',
        'sqlalchemy-migrate'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
