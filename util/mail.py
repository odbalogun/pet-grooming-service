from mailqueue.models import MailerMessage


def send_mail(subject, message, to, sender='info@appetments.com'):
    mail = MailerMessage()
    mail.subject = subject
    mail.to_address = to
    mail.from_address = sender
    mail.html_content = message
    mail.app = 'Appetments'
    mail.save()
