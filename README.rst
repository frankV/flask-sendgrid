flask-sendgrid
==============

|PyPI version| |Travis Build| |Coverage Status|

Flask plugin for sending emails with `SendGrid`_.

Provides full support for all Twilio SendGrid `Web API v3`_ endpoints, including `v3 /mail/send`_.


Installation
------------

.. code-block:: bash

    pip install flask-sendgrid


Usage
-----

.. code-block:: python

    from flask_sendgrid import SendGrid
    app = Flask(__name__)
    app.config['SENDGRID_API_KEY'] = 'your api key'
    app.config['SENDGRID_DEFAULT_FROM'] = 'admin@yourdomain.com'
    mail = SendGrid(app)

    # send multiple recipients; backwards compatible with Flask-Mandrill
    mail.send_email(
        from_email='someone@yourdomain.com',
        to_email=[{'email': 'test1@example.com'}, {'email': 'test2@example.com'}],
        subject='Subject',
        text='Body',
    )

    # send single recipient; single email as string
    mail.send_email(
        from_email='someone@yourdomain.com',
        to_email='test@example.com',
        subject='Subject',
        text='Body',
    )

    # send single recipient; single email as sendgrid.mail.helpers.Email object
    mail.send_email(
        from_email='someone@yourdomain.com',
        to_email=Email('test@example.com'),
        subject='Subject',
        text='Body',
    )

    # send multiple recipients; list of emails as sendgrid.mail.helpers.Email object
    mail.send_email(
        from_email='someone@yourdomain.com',
        to_email=[Email('test1@example.com'), Email('test2@example.com')],
        subject='Subject',
        text='Body',
    )


For additional information about mail parameters: `SendGrid Web API
Mail`_

.. _SendGrid: https://sendgrid.com/
.. _Flask-Mandrill: https://github.com/volker48/flask-mandrill
.. _Web API v3: https://sendgrid.com/docs/API_Reference/Web_API_v3/index.html
.. _v3 /mail/send: https://sendgrid.com/blog/introducing-v3mailsend-sendgrids-new-mail-endpoint
.. _SendGrid Web API Mail: https://sendgrid.com/docs/API_Reference/Web_API_v3/Mail/index.html#-Request-Body-Parameters

.. |PyPI version| image:: https://badge.fury.io/py/Flask-SendGrid.svg
   :target: https://pypi.python.org/pypi/Flask-SendGrid/
.. |Travis Build| image:: https://travis-ci.org/frankV/flask-sendgrid.svg?branch=master
   :target: https://travis-ci.org/frankV/flask-sendgrid
.. |Coverage Status| image:: https://coveralls.io/repos/github/frankV/flask-sendgrid/badge.svg?branch=master
   :target: https://coveralls.io/github/frankV/flask-sendgrid?branch=master
