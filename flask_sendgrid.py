from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Content


class SendGrid(object):
    app = None
    api_key = None
    default_from = None

    def __init__(self, app=None, **opts):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.api_key = app.config['SENDGRID_API_KEY']
        self.default_from = app.config['SENDGRID_DEFAULT_FROM']

    def send_email(self, to_email, subject, from_email=None,
                   html=None, text=None):
        if not any([from_email, self.default_from]):
            raise ValueError("Missing from email and no default.")
        if not any([html, text]):
            raise ValueError("Missing html or text.")

        sg = SendGridAPIClient(apikey=self.api_key)

        mail = Mail(
            from_email=Email(from_email or self.default_from),
            subject=subject,
            to_email=Email(to_email),
            content=Content("text/html", html) if html
                else Content("text/plain", text),
        )

        return sg.client.mail.send.post(request_body=mail.get())

        # Use a template if specified. 
        # See https://github.com/sendgrid/sendgrid-python/blob/master/examples/example_v2.py
#         if opts.get('template_id', None):
#             message.add_filter('templates', 'enable', '1')
#             message.add_filter('templates', 'template_id', opts['template_id'])

#             substitutions = opts.get('substitutions', dict()).items()
#             for key, value in substitutions:
#                 message.add_substitution(key, value)
