from mailqueue.models import MailerMessage
import random
import string


def send_mail(subject, message, to, sender='info@appetments.com'):
    """
    Send an email
    :param subject: String subject of the email
    :param message: Text body of the email
    :param to: String email receiver
    :param sender: String email sender
    """
    mail = MailerMessage()
    mail.subject = subject
    mail.to_address = to
    mail.from_address = sender
    mail.html_content = message
    mail.app = 'Appetments'
    mail.save()


def random_string(length):
    """
    Creates a random string
    :param length: String length of the string to return
    :return: String
    """
    random_list = []
    for i in range(length):
        random_list.append(random.choice(string.ascii_uppercase + string.digits))
    return ''.join(random_list)