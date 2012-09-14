"""
hipflask
-------------

Description goes here...


"""
from setuptools import setup


setup(
    name='hipflask',
    version='0.2',
    url='http://github.com/robertfw/hipflask',
    license='MIT',
    author='Robert Warner',
    author_email='radicalphoenix@gmail.com',
    description='Quickstart tool for setting up common flask extensions',
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
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)