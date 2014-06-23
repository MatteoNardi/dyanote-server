from django.contrib import admin
from api.models import Page, ActivationKey

# Add the Page and ActivationKey models to the admin interface.

class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title')
    list_filter = ('author', 'created')
    search_fields = ('title', 'body')

class ActivationKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'key')

admin.site.register(Page, PageAdmin)
admin.site.register(ActivationKey, ActivationKeyAdmin)
