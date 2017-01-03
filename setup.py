"""
Flask-SendGrid
==============

A Flask Extension to bridge between `Flask-Mandrill <https://github.com/volker48/flask-mandrill>`_
and sending emails with `SendGrid <http://www.sendgrid.com/>`_

Installation
````````````

.. code:: bash

    $ pip install flask-sendgrid


Usage
`````

.. code:: python

        from flask import Flask
        from flask.ext.sendgrid import SendGrid

        app = Flask(__name__)
        app.config['SENDGRID_API_KEY'] = 'your api key'
        sendgrid = SendGrid(app)
        sendgrid.send_email(
            from_email='someone@yourdomain.com',
            to_email='someoneelse@someotherdomain.com',
            subject='Subject'
            text='Body',
        )
"""

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


def get_requirements(suffix=''):
    with open('requirements%s.txt' % suffix) as f:
        rv = f.read().splitlines()
    return rv


def get_version():
    with open('flask_sendgrid.py', 'r') as fd:
        for line in fd:
            if line.startswith('__version__ = '):
                return line.split()[-1].strip().strip("'")


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '-v',
            '-xrs',
            '--cov', '.',
            '--cov-report', 'term-missing',
            '--pep8',
            '--flakes',
            '--cache-clear'
        ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

_version = get_version()


setup(
    name='Flask-SendGrid',
    version=_version,
    url='http://github.com/frankv/flask-sendgrid',
    download_url='https://github.com/frankv/flask-sendgrid/tarball/' + _version,
    license='MIT',
    author='Frank Valcarcel',
    author_email='frank@cuttlesoft.com',
    description='Adds SendGrid support to Flask applications',
    long_description=open('README.md').read() + '\n\n' + open('HISTORY.rst').read(),
    keywords=['Flask', 'SendGrid', 'email', 'smtp'],
    py_modules=['flask_sendgrid'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask~=0.10.1',
        'SendGrid~=3.0'],
    tests_require=get_requirements('-test'),
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules']
)
