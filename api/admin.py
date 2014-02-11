from django.contrib import admin
from api.models import Page

# Add the Page model to the admin interface.

class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title')
    list_filter = ('author', 'created')
    search_fields = ('title', 'body')

admin.site.register(Page, PageAdmin)
