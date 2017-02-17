from django.views.generic import CreateView
from . import forms
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


class SubscribeView(CreateView):
    form_class = forms.SubscribeForm
    template_name = 'newsletter/subscribe_form.html'
    success_url = reverse_lazy('newsletter_subscribe')

    def render_to_response(self, context, **response_kwargs):
        html = render_to_string(
            self.template_name, context, request=self.request)
        data = {'html': html}
        if getattr(self, 'success', False):
            data['message'] = str(_("You successfully subscribed"))
        return JsonResponse(data)

    def form_valid(self, form):
        self.object = form.save()
        self.success = True
        self.request.method = 'GET'
        return self.get(self.request)
