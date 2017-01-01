import sendgrid


class FlaskSendGrid(object):
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

    def send_email(self, **opts):
        if not opts.get('from_email', None) and not self.default_from:
            raise ValueError('No from email or default_from was configured')

        client = sendgrid.SendGridClient(self.api_key)
        message = sendgrid.Mail()

        for _ in opts['to']:
            message.add_to(_['email'])

        # Use a template if specified. 
        # See https://github.com/sendgrid/sendgrid-python/blob/master/examples/example_v2.py
        if opts.get('template_id', None):
            message.add_filter('templates', 'enable', '1')
            message.add_filter('templates', 'template_id', opts['template_id'])

            substitutions = opts.get('substitutions', dict()).items()
            for key, value in substitutions:
                message.add_substitution(key, value)

        message.set_from(opts.get('from_email', None) or self.default_from)
        message.set_subject(opts['subject'])

        if opts.get('html', None):
            message.set_html(opts['html'])
        elif opts.get('text', None):
            message.set_html(opts['text'])

        return client.send(message)
