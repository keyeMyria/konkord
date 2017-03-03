from django.contrib import admin
from .models import ResponseLog
from django.utils.translation import ugettext_lazy as _


@admin.register(ResponseLog)
class ResponseLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'referer',
        'url_to',
        'count',
        'update_date',
        'status_code'
    )
    search_fields = ['url']
    list_filter = ('status_code',)

    def url_to(self, obj):
        html = '''<a href="%s" target="_blank" style="
        max-width: 350px; overflow-x: auto; height: 32px;
        display:block;white-space: nowrap;">%s</a>''' % (obj.url, obj.url)
        return html

    url_to.allow_tags = True
    url_to.short_description = _("Url")