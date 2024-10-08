import os
import logging

from django.core.mail import EmailMessage, EmailMultiAlternatives


class Mail:

    def __init__(self, multipart=False):
        self.multipart = multipart
        self.mailer = EmailMessage
        if self.multipart:
            self.mailer = EmailMultiAlternatives

    def send_mail(self, args=None):
        try:
            if args.get('to'):
                text_content = args.get('text_content') if args.get('text_content') else None
                html_content = args.get('html_content') if args.get('html_content') else None

                mail = self.mailer(
                    subject=args.get('subject') if args.get('subject') else "",
                    body=text_content,
                    to=args.get('to'),
                    cc=args.get('cc') if args.get('cc') else None,
                    bcc=args.get('bcc') if args.get('bcc') else None,
                    attachments=args.get('attachments') if args.get('attachments') else None,
                    reply_to=[os.getenv('EMAIL_NO_REPLY')],
                )
                if html_content and self.multipart:
                    mail.attach_alternative(html_content, "text/html")
                mail.send()
        except Exception as e:
            logging.exception(str(e))
