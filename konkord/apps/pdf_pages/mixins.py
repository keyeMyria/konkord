# -*- coding: utf-8 -*-
import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings


class PDFPageMixin(object):

    def get_pdf_template(self):
        try:
            return self.pdf_template
        except AttributeError:
            return self.get_template_names()

    def render_to_response(self, context):
        if self.request.GET.get('pdf') or self.request.POST.get('pdf'):
            context['MEDIA_ROOT'] = settings.MEDIA_ROOT
            context['MEDIA_URL'] = settings.MEDIA_URL
            context['PDF'] = True
            html = render_to_string(
                self.get_pdf_template(), context, request=self.request)
            html = html.replace(
                settings.MEDIA_URL, settings.MEDIA_ROOT + (
                    '/'
                    if settings.MEDIA_URL.endswith('/')
                       and not settings.MEDIA_ROOT.endswith('/') else '')

            ).replace(
                settings.STATIC_URL, settings.STATIC_ROOT + '/'
            )
            pdf = pdfkit.from_string(
                html, False
            )
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            return super(PDFPageMixin, self).render_to_response(context)
