import unittest
from mock import MagicMock
from flask_sendgrid import SendGrid

# Set up test API key for emails
app = MagicMock()
app.config = {}
app.config['TESTING'] = True
app.config['SENDGRID_API_KEY'] = '12345'
app.config['SENDGRID_DEFAULT_FROM'] = 'from'


class SendGridTest(unittest.TestCase):

    def setUp(self):
        self.mail = SendGrid(app)

    def test_get_api_key(self):
        self.assertEqual(self.mail.api_key, app.config['SENDGRID_API_KEY'])

    def test_fails_no_key(self):
        mail = SendGrid()
        self.assertRaises(TypeError, mail.send_email)

    def test_fails_no_sender(self):
        mail = SendGrid()
        self.assertRaises(TypeError, mail.send_email, key='ABCDEFG')
