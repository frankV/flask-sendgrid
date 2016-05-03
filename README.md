flask-sendgrid
==============

Flask plugin to simplify sending emails through SendGrid. Adapted from [Flask-Mandrill](https://github.com/volker48/flask-mandrill)
to make migrating from Mandrill to SendGrid easier for developers.


Installation
------------

    pip install flask-sendgrid

Usage
-----

    from flask.ext.sendgrid import FlaskSendGrid

    app = Flask(__name__)
    app.config['SENDGRID_API_KEY'] = 'your api key'
    app.config['SENDGRID_DEFAULT_FROM'] = 'admin@yourdomain.com'
    sendgrid = FlaskSendGrid(app)
    sendgrid.send_email(
        from_email='someone@yourdomain.com',
        subject='Subject',
        template_id='some_id',
        substitutions={ ':name': 'Peter Piper' },
        to=[{'email': 'someone@somedomain.com'}, {'email': 'someoneelse@someotherdomain.com'}],
        text='Hello World'
    )

Using templates (`template_id` and `substitutions`) is purely optional.


For additional information about mail parameters: [SendGrid Web API Mail](https://sendgrid.com/docs/API_Reference/Web_API/mail.html#parameters-mail)
