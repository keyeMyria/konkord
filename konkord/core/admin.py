from django.contrib import admin
from django.contrib.redirects.admin import (
    RedirectAdmin as DefaultRedirectAdmin
)
from django.contrib.redirects.models import Redirect
from django.template.response import TemplateResponse
from core.forms import RedirectsImportForm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from django.contrib import messages
admin.site.unregister(Redirect)


@admin.register(Redirect)
class RedirectAdmin(DefaultRedirectAdmin):

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