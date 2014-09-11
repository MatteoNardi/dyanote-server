import hashlib
import random

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from api.models import Page


def get_server_url():
    ''' Get the url of the api server. Eg. https://api.dyanote.com '''
    return Site.objects.get(name='Server').domain

def get_client_url():
    ''' Get the url of the client. Eg. http://dyanote.com '''
    return Site.objects.get(name='Client').domain

def mail_user(user, subject, template, **kwargs):
    """ Send a mail to the user """
    params = kwargs
    params["email"] = user.email
    params["site"] = get_server_url()
    msg = render_to_string(template, params)
    send_mail(subject, msg, 'Dyanote', [user.email])

def user_exists(username):
	return username and User.objects.filter(username=username).count()

def generate_activation_key(user):
    ''' Given a user, return a random string which can be used as an activation key'''
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    email = user.email
    if isinstance(email, unicode):
        email = email.encode('utf-8')
    return hashlib.sha1(salt+email).hexdigest()

def setup_default_notes(user):
    ''' Given a user who has just subscribed, create a default set of notes for him. '''
    templates = [
        # Title, filename, parent filename
        ('Index', 'root.xml', None),
        ('Archive', 'archive.xml', None),
        ('Todo', 'todo.xml', 'root.xml'),
        ('Shopping List', 'shopping.xml', 'todo.xml'),
        ('Projects', 'projects.xml', 'root.xml'),
        ('Incubation List', 'incubation.xml', 'root.xml'),
        ('Books to read', 'books.xml', 'incubation.xml'),
        ('Movies to read', 'movies.xml', 'incubation.xml'),
        ('Citations', 'citations.xml', 'incubation.xml')
    ]
    notes = {}
    for title, filename, _ in templates:
        flags = Page.NORMAL
        if filename == 'root.xml': flags = Page.ROOT
        if filename == 'archive.xml': flags = Page.ARCHIVE
        notes[filename] = Page.objects.create(title=title, parent=None, author=user, flags=flags)

    urls = { filename[:-4]: get_note_url(note) for filename, note in notes.items()}
    for note in notes.values():
        _, filename, parent = next(t for t in templates if t[0] == note.title)
        note.body = render_to_string('api/default_notes/' + filename, urls)
        if parent:
            note.parent = notes[parent]
        note.save()

def get_note_url(note):
    ''' Given a note, return its url '''
    kwargs = {
        'username': note.author.email,
        'pk': note.id
    }
    return get_server_url() + reverse('page-detail', kwargs=kwargs)
