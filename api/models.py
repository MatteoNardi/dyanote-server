from django.db import models

class Page(models.Model):
    """A Page in Dyanote."""
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, default='')
    parent = models.ForeignKey('api.Page', null=True, blank=True, related_name='children')
    body = models.TextField(blank=True, default='')
    author = models.ForeignKey('auth.User', related_name='pages')

    NORMAL = 0
    ROOT = 1
    TRASH = 2
    FLAGS = (
        (NORMAL, 'Normal page'),
        (ROOT, 'Root page'),
        (TRASH, 'Trash page'),
    )
    flags = models.IntegerField(choices=FLAGS, default=NORMAL)

    class Meta:
        ordering = ('created',)
