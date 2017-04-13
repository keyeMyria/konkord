# -*- coding: utf-8 -*-
from . import models
from django import forms
from mail.utils import send_email, render
from django.conf import settings


class SubscribeForm(forms.ModelForm):

    mail_template = 'newsletter/subscribe_mail.html'
    mail_subject = 'newsletter/subscribe_mail_subject.html'

    class Meta:
        model = models.Subscribe
        fields = '__all__'

    def send_email(self, obj):
        to_email = settings.SITE_EMAIL
        subject = render(self.mail_subject)
        html = render(
            self.mail_template, **{'subscribe': obj}
        )
        if to_email:
            send_email(subject=subject, text=html, html=html, to=[to_email])

    def save(self, commit=True):
        obj = super(SubscribeForm, self).save(commit)
        if commit:
            self.send_email(obj)
        return obj
