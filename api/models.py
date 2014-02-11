from django.db import models
from django.core.exceptions import ValidationError

class Page(models.Model):
    """A Page in Dyanote."""
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, default='')
    parent = models.ForeignKey('api.Page', null=True, blank=True, related_name='children')
    body = models.TextField(blank=True, default='')
    author = models.ForeignKey('auth.User', related_name='pages')

    NORMAL = 0
    ROOT = 1
    ARCHIVE = 2
    FLAGS = (
        (NORMAL, 'Normal page'),
        (ROOT, 'Root page'),
        (ARCHIVE, 'Archive page'),
    )
    flags = models.IntegerField(choices=FLAGS, default=NORMAL)

    class Meta:
        ordering = ('created',)

    def clean(self):
        if self.parent is None and self.flags is Page.NORMAL:
            raise ValidationError("Parent is required in normal pages.")

