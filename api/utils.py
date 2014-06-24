from django.template.loader import render_to_string
from django.core.mail import send_mail


def mail_user(user, subject, template):
	""" Send a mail to the user """
	params = kwargs
	params["email"] = user.email
	msg = render_to_string(template, params)
    send_mail(subject, msg, 'Dyanote', [user.email])


