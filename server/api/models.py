from django.db import models

class Page(models.Model):
    """A Page in Dyanote."""
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField(blank=True, default='')
    author = models.ForeignKey('auth.User', related_name='pages')

    class Meta:
        ordering = ('created',)
