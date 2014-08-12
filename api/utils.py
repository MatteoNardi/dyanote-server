from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

def mail_user(user, subject, template, **kwargs):
    """ Send a mail to the user """
    params = kwargs
    params["email"] = user.email
    params["site"] = Site.objects.get_current().domain
    msg = render_to_string(template, params)
    send_mail(subject, msg, 'Dyanote', [user.email])


def user_exists(username):
	return username and User.objects.filter(username=username).count()

