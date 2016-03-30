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
            to=[{'email': 'someoneelse@someotherdomain.com'}],
            text='Hello World'
        )
"""

from setuptools import setup


setup(
    name='Flask-SendGrid',
    version='0.1.0',
    url='http://github.com/frankv/flask-sendgrid',
    download_url='https://github.com/frankv/flask-sendgrid/tarball/0.1.0',
    license='MIT',
    author='Frank Valcarcel',
    author_email='frank@cuttlesoft.com',
    description='Adds SendGrid support to Flask applications',
    long_description=__doc__ + '\n\n' + open('HISTORY.rst').read(),
    keywords=['Flask', 'SendGrid', 'email', 'smtp'],
    py_modules=['flask_sendgrid'],
    zip_safe=False,
    platforms='any',
    install_requires=['Flask', 'SendGrid'],
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
