flask-sendgrid
==============


<!-- [![Py version](https://img.shields.io/pypi/pyversions/flask-sendgrid.svg)](https://pypi.python.org/pypi/Flask-SendGrid/) -->
<!-- [![PyPI Downloads](https://img.shields.io/pypi/dm/Flask-SendGrid.svg)](https://pypi.python.org/pypi/Flask-SendGrid/) -->
[![PyPI version](https://badge.fury.io/py/Flask-SendGrid.svg)](https://pypi.python.org/pypi/Flask-SendGrid/)
[![Travis Build](https://travis-ci.org/frankV/flask-sendgrid.svg?branch=master)](https://travis-ci.org/frankV/flask-sendgrid)
[![Coverage Status](https://coveralls.io/repos/github/frankV/flask-sendgrid/badge.svg?branch=master)](https://coveralls.io/github/frankV/flask-sendgrid?branch=master)

Flask plugin to simplify sending emails through [SendGrid](https://sendgrid.com/). Adapted from [Flask-Mandrill](https://github.com/volker48/flask-mandrill)
to make migrating from Mandrill to SendGrid easier for developers.

Now updated to support SendGrid [Web API v3](https://sendgrid.com/docs/API_Reference/Web_API_v3/index.html) endpoints, including the new [v3 /mail/send](https://sendgrid.com/blog/introducing-v3mailsend-sendgrids-new-mail-endpoint). Still maintains backwards compatibility with Flask-Mandrill `mail` function.

Existing `send_email` method does not support all functions of the newly updated SendGrid Mail (`sendgrid.helpers.mail.Mail`). Full support will be updated in a later release.


Installation
------------

    pip install flask-sendgrid

Usage
-----
```python
from flask.ext.sendgrid import SendGrid

app = Flask(__name__)
app.config['SENDGRID_API_KEY'] = 'your api key'
app.config['SENDGRID_DEFAULT_FROM'] = 'admin@yourdomain.com'
mail = SendGrid(app)

# send multiple recipients; backwards compatible with Flask-Mandrill
mail.send_email(
    from_email='someone@yourdomain.com',
    to_email=[{'email': 'test1@example.com'}, {'email': 'test2@example.com'}],
    subject='Subject'
    text='Body',
)

# send single recipient; single email as string
mail.send_email(
    from_email='someone@yourdomain.com',
    to_email='test@example.com',
    subject='Subject'
    text='Body',
)

# send single recipient; single email as sendgrid.mail.helpers.Email object
mail.send_email(
    from_email='someone@yourdomain.com',
    to_email=Email('test@example.com'),
    subject='Subject'
    text='Body',
)

# send multiple recipients; list of emails as sendgrid.mail.helpers.Email object
mail.send_email(
    from_email='someone@yourdomain.com',
    to_email=[Email('test1@example.com'), Email('test2@example.com')],
    subject='Subject'
    text='Body',
)
```

For additional information about mail parameters: [SendGrid Web API Mail](https://sendgrid.com/docs/API_Reference/Web_API_v3/Mail/index.html#-Request-Body-Parameters)
