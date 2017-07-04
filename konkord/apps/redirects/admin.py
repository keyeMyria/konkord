from django.conf.urls import url
from django.contrib import admin
from django.contrib import messages
from redirects.models import Redirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from redirects.forms import RedirectsImportForm


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path')
    list_filter = ('site',)
    search_fields = ('old_path', 'new_path')
    radio_fields = {'site': admin.VERTICAL}

    def get_urls(self):
        urls = super(RedirectAdmin, self).get_urls()
        return [
            url(
                r'^redirects_import/$',
                self.admin_site.admin_view(self.redirects_import_view),
                name='redirects_import'
            )
        ] + urls

    def redirects_import_view(self, request):
        if request.method == 'GET':
            form = RedirectsImportForm()
        else:
            form = RedirectsImportForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, _('Redirects imported successfully'))
                return redirect(
                    reverse("admin:redirects_redirect_changelist")
                )
        context = dict(
            self.admin_site.each_context(request),
            form=form
        )
        return TemplateResponse(
            request, "admin/redirects/import_form.html", context)

