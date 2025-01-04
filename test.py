import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DaLinci.settings")
django.setup()

from django.core.mail import send_mail

def send_email():
    subject = "Пример письма"
    message = "Это тестовое сообщение"
    email_from = "playlexei@yandex.ru"
    recipient_list = ["workkovanoff.al@yandex.ru"]

    send_mail(subject, message, email_from, recipient_list)
    print(12)
if __name__ == '__main__':
    send_email()
