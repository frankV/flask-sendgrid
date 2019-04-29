# -*- coding: utf-8 -*-
"""
    test.test_extension.py
    ~~~~~~~~~~~~~~~~~~~~~~
    Unit Tests for Flask-SendGrid
"""
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import json
from mock import MagicMock, Mock, patch
from sendgrid.helpers.mail import *
from flask_sendgrid import SendGrid


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
        self.assertRaises(TypeError, self.mail.send_email)

    def test_fails_no_sender(self):
        mail = SendGrid()
        mail.api_key = app.config['SENDGRID_API_KEY']
        with self.assertRaises(ValueError):
            mail.send_email(subject='subject', to_email='to')

    def test_fails_no_content(self):
        mail = SendGrid()
        mail.api_key = app.config['SENDGRID_API_KEY']
        with self.assertRaises(ValueError):
            mail.send_email(subject='subject', from_email='from', to_email='to')

    @patch('python_http_client.Client._make_request')
    def test_mandrill_compat_email_send(self, mock_client):
        mock = Mock()
        mock.return_value.ok = True
        mock_client.return_value = mock

        self.mail.send_email(
            subject='Subject',
            to_email='test@example.com',
            html='<h2>html</h2>'
        )

        self.assertEqual(json.dumps(self.mail.get(), sort_keys=True), '{"content": [{"type": "text/html", "value": "<h2>html</h2>"}], "from": {"name": "from"}, "personalizations": [{"to": [{"email": "test@example.com"}]}], "subject": "Subject"}')

    @patch('python_http_client.Client._make_request')
    def test_mandrill_compat_single_recipient(self, mock_client):
        mock = Mock()
        mock.return_value.ok = True
        mock_client.return_value = mock

        self.mail.send_email(
            subject='Subject',
            to_email=[{'email': 'test@example.com'}],
            html='<h2>html</h2>'
        )

        self.assertEqual(json.dumps(self.mail.get(), sort_keys=True), '{"content": [{"type": "text/html", "value": "<h2>html</h2>"}], "from": {"name": "from"}, "personalizations": [{"to": [{"email": "test@example.com"}]}], "subject": "Subject"}')

    @patch('python_http_client.Client._make_request')
    def test_mandrill_compat_multiple_recipient(self, mock_client):
        mock = Mock()
        mock.return_value.ok = True
        mock_client.return_value = mock

        self.mail.send_email(
            subject='Subject',
            to_email=[{'email': 'test1@example.com'}, {'email': 'test2@example.com'}],
            html='<h2>html</h2>'
        )

        self.assertEqual(json.dumps(self.mail.get(), sort_keys=True), '{"content": [{"type": "text/html", "value": "<h2>html</h2>"}], "from": {"name": "from"}, "personalizations": [{"to": [{"email": "test1@example.com"}, {"email": "test2@example.com"}]}], "subject": "Subject"}')

    @patch('python_http_client.Client._make_request')
    def test_single_recipient_email_object(self, mock_client):
        mock = Mock()
        mock.return_value.ok = True
        mock_client.return_value = mock

        self.mail.send_email(
            subject='Subject',
            to_email=Email('test1@example.com'),
            html='<h2>html</h2>'
        )

        self.assertEqual(json.dumps(self.mail.get(), sort_keys=True), '{"content": [{"type": "text/html", "value": "<h2>html</h2>"}], "from": {"name": "from"}, "personalizations": [{"to": [{"email": "test1@example.com"}]}], "subject": "Subject"}')

    @patch('python_http_client.Client._make_request')
    def test_multiple_recipient_email_object(self, mock_client):
        mock = Mock()
        mock.return_value.ok = True
        mock_client.return_value = mock

        self.mail.send_email(
            subject='Subject',
            to_email=[Email('test1@example.com'), Email('test2@example.com')],
            html='<h2>html</h2>'
        )

        self.assertEqual(json.dumps(self.mail.get(), sort_keys=True), '{"content": [{"type": "text/html", "value": "<h2>html</h2>"}], "from": {"name": "from"}, "personalizations": [{"to": [{"email": "test1@example.com"}, {"email": "test2@example.com"}]}], "subject": "Subject"}')

    @patch('python_http_client.Client._make_request')
    def test_hello_email(self, mock_client):
        self.maxDiff = None

        mock = Mock()
        mock.return_value.ok = True
        mock_client.return_value = mock

        """Minimum required to send an email"""

        self.mail.from_email = Email("test@example.com")
        self.mail.subject = "Hello World from the SendGrid Python Library"

        personalization = Personalization()
        personalization.add_to(Email("test@example.com"))
        self.mail.add_personalization(personalization)

        self.mail.add_content(Content("text/plain", "some text here"))
        self.mail.add_content(Content("text/html", "<html><body>some text here</body></html>"))

        self.assertEqual(json.dumps(self.mail.get(), sort_keys=True), '{"content": [{"type": "text/plain", "value": "some text here"}, {"type": "text/html", "value": "<html><body>some text here</body></html>"}], "from": {"email": "test@example.com"}, "personalizations": [{"to": [{"email": "test@example.com"}]}], "subject": "Hello World from the SendGrid Python Library"}')

    @patch('python_http_client.Client._make_request')
    def test_kitchenSink(self, mock_client):
        self.maxDiff = None

        mock = Mock()
        mock.return_value.ok = True
        mock_client.return_value = mock

        """All settings set"""

        self.mail.from_email = Email("test@example.com", "Example User")

        self.mail.subject = Subject("Hello World from the SendGrid Python Library")

        personalization = Personalization()
        personalization.add_to(Email("test@example.com", "Example User"))
        personalization.add_to(Email("test@example.com", "Example User"))
        personalization.add_cc(Email("test@example.com", "Example User"))
        personalization.add_cc(Email("test@example.com", "Example User"))
        personalization.add_bcc(Email("test@example.com"))
        personalization.add_bcc(Email("test@example.com"))
        personalization.subject = "Hello World from the Personalized SendGrid Python Library"
        personalization.add_header(Header("X-Test", "test"))
        personalization.add_header(Header("X-Mock", "true"))
        personalization.add_substitution(Substitution("%name%", "Example User"))
        personalization.add_substitution(Substitution("%city%", "Denver"))
        personalization.add_custom_arg(CustomArg("user_id", "343"))
        personalization.add_custom_arg(CustomArg("type", "marketing"))
        personalization.send_at = 1443636843
        self.mail.add_personalization(personalization)

        personalization2 = Personalization()
        personalization2.add_to(Email("test@example.com", "Example User"))
        personalization2.add_to(Email("test@example.com", "Example User"))
        personalization2.add_cc(Email("test@example.com", "Example User"))
        personalization2.add_cc(Email("test@example.com", "Example User"))
        personalization2.add_bcc(Email("test@example.com"))
        personalization2.add_bcc(Email("test@example.com"))
        personalization2.subject = "Hello World from the Personalized SendGrid Python Library"
        personalization2.add_header(Header("X-Test", "test"))
        personalization2.add_header(Header("X-Mock", "true"))
        personalization2.add_substitution(Substitution("%name%", "Example User"))
        personalization2.add_substitution(Substitution("%city%", "Denver"))
        personalization2.add_custom_arg(CustomArg("user_id", "343"))
        personalization2.add_custom_arg(CustomArg("type", "marketing"))
        personalization2.send_at = 1443636843
        self.mail.add_personalization(personalization2)

        self.mail.add_content(Content("text/plain", "some text here"))
        self.mail.add_content(Content("text/html", "<html><body>some text here</body></html>"))

        attachment = Attachment()
        attachment.content = FileContent("TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNlY3RldHVyIGFkaXBpc2NpbmcgZWxpdC4gQ3JhcyBwdW12")
        attachment.type = FileType("application/pdf")
        attachment.filename = FileName("balance_001.pdf")
        attachment.disposition = Disposition("attachment")
        attachment.content_id = ContentId("Balance Sheet")
        self.mail.add_attachment(attachment)

        attachment2 = Attachment()
        attachment2.content = FileContent("BwdW")
        attachment2.type = FileType("image/png")
        attachment2.filename = FileName("banner.png")
        attachment2.disposition = Disposition("inline")
        attachment2.content_id = ContentId("Banner")
        self.mail.add_attachment(attachment2)

        self.mail.template_id = TemplateId("13b8f94f-bcae-4ec6-b752-70d6cb59f932")

        self.mail.add_section(Section("%section1%", "Substitution Text for Section 1"))
        self.mail.add_section(Section("%section2%", "Substitution Text for Section 2"))

        self.mail.add_header(Header("X-Test1", "test1"))
        self.mail.add_header(Header("X-Test3", "test2"))

        #This can not take a dic until the issue has been resolved. Issue 793 currently unresolved https://github.com/sendgrid/sendgrid-python/issues/793
        self.mail.add_header(Header("X-Test4", "test4"))

        self.mail.add_category(Category("May"))
        self.mail.add_category(Category("2016"))

        self.mail.add_custom_arg(CustomArg("campaign", "welcome"))
        self.mail.add_custom_arg(CustomArg("weekday", "morning"))

        self.mail.send_at = SendAt(1443636842)

        self.mail.batch_id = BatchId("sendgrid_batch_id")

        self.mail.asm = Asm(99, [4, 5, 6, 7, 8])

        self.mail.ip_pool_name = IpPoolName("24")

        mail_settings = MailSettings()
        mail_settings.bcc_settings = BccSettings(True, BccSettingsEmail("test@example.com"))
        mail_settings.bypass_list_management = BypassListManagement(True)
        mail_settings.footer_settings = FooterSettings(True, FooterText("Footer Text"), FooterHtml("<html><body>Footer Text</body></html>"))
        mail_settings.sandbox_mode = SandBoxMode(True)
        mail_settings.spam_check = SpamCheck(True, 1, "https://spamcatcher.sendgrid.com")
        self.mail.mail_settings = mail_settings

        tracking_settings = TrackingSettings()
        tracking_settings.click_tracking = ClickTracking(True, True)
        tracking_settings.open_tracking = OpenTracking(True, OpenTrackingSubstitutionTag("Optional tag to replace with the open image in the body of the message"))
        tracking_settings.subscription_tracking = SubscriptionTracking(True, SubscriptionText("text to insert into the text/plain portion of the message"), SubscriptionHtml("<html><body>html to insert into the text/html portion of the message</body></html>"), SubscriptionSubstitutionTag("Optional tag to replace with the open image in the body of the message"))
        tracking_settings.ganalytics = Ganalytics(True, UtmSource("some source"), UtmMedium("some medium"), UtmTerm("some term"), UtmContent("some content"), UtmCampaign("some campaign"))
        self.mail.tracking_settings = tracking_settings

        self.mail.reply_to = ReplyTo("test@example.com")
        print(json.dumps(self.mail.get(), sort_keys=True))
        self.assertEqual(json.dumps(self.mail.get(), sort_keys=True), '{"asm": {"group_id": 99, "groups_to_display": [4, 5, 6, 7, 8]}, "attachments": [{"content": "TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNlY3RldHVyIGFkaXBpc2NpbmcgZWxpdC4gQ3JhcyBwdW12", "content_id": "Balance Sheet", "disposition": "attachment", "filename": "balance_001.pdf", "type": "application/pdf"}, {"content": "BwdW", "content_id": "Banner", "disposition": "inline", "filename": "banner.png", "type": "image/png"}], "batch_id": "sendgrid_batch_id", "categories": ["May", "2016"], "content": [{"type": "text/plain", "value": "some text here"}, {"type": "text/html", "value": "<html><body>some text here</body></html>"}], "custom_args": {"campaign": "welcome", "weekday": "morning"}, "from": {"email": "test@example.com", "name": "Example User"}, "headers": {"X-Test1": "test1", "X-Test3": "test2", "X-Test4": "test4"}, "ip_pool_name": "24", "mail_settings": {"bcc": {"email": "test@example.com", "enable": true}, "bypass_list_management": {"enable": true}, "footer": {"enable": true, "html": "<html><body>Footer Text</body></html>", "text": "Footer Text"}, "sandbox_mode": {"enable": true}, "spam_check": {"enable": true, "post_to_url": "https://spamcatcher.sendgrid.com", "threshold": 1}}, "personalizations": [{"bcc": [{"email": "test@example.com"}, {"email": "test@example.com"}], "cc": [{"email": "test@example.com", "name": "Example User"}, {"email": "test@example.com", "name": "Example User"}], "custom_args": {"type": "marketing", "user_id": "343"}, "headers": {"X-Mock": "true", "X-Test": "test"}, "send_at": 1443636843, "subject": "Hello World from the Personalized SendGrid Python Library", "substitutions": {"%city%": "Denver", "%name%": "Example User"}, "to": [{"email": "test@example.com", "name": "Example User"}, {"email": "test@example.com", "name": "Example User"}]}, {"bcc": [{"email": "test@example.com"}, {"email": "test@example.com"}], "cc": [{"email": "test@example.com", "name": "Example User"}, {"email": "test@example.com", "name": "Example User"}], "custom_args": {"type": "marketing", "user_id": "343"}, "headers": {"X-Mock": "true", "X-Test": "test"}, "send_at": 1443636843, "subject": "Hello World from the Personalized SendGrid Python Library", "substitutions": {"%city%": "Denver", "%name%": "Example User"}, "to": [{"email": "test@example.com", "name": "Example User"}, {"email": "test@example.com", "name": "Example User"}]}], "reply_to": {"email": "test@example.com"}, "sections": {"%section1%": "Substitution Text for Section 1", "%section2%": "Substitution Text for Section 2"}, "send_at": 1443636842, "subject": "Hello World from the SendGrid Python Library", "template_id": "13b8f94f-bcae-4ec6-b752-70d6cb59f932", "tracking_settings": {"click_tracking": {"enable": true, "enable_text": true}, "ganalytics": {"enable": true, "utm_campaign": "some campaign", "utm_content": "some content", "utm_medium": "some medium", "utm_source": "some source", "utm_term": "some term"}, "open_tracking": {"enable": true, "substitution_tag": "Optional tag to replace with the open image in the body of the message"}, "subscription_tracking": {"enable": true, "html": "<html><body>html to insert into the text/html portion of the message</body></html>", "substitution_tag": "Optional tag to replace with the open image in the body of the message", "text": "text to insert into the text/plain portion of the message"}}}')
