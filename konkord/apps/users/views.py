# -*- coding: utf-8 -*-
from django.views.generic import View, DetailView, FormView, TemplateView
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
)
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
# from django.utils import timezone
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from users.forms import (
    RegisterForm, LoginForm, UserResetPasswordForm
)
from users.models import User  # , Email, Phone
from django.http import Http404
from core.mixins import MetaMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from core.mixins import JSONResponseMixin


class LoginView(View):

    mail_template = 'registration/registration_mail.html'
    mail_subject = 'registration/registration_mail_subject.html'

    def get(self, request):
        context = {
            'login_form': LoginForm(request),
            'register_form': RegisterForm()
        }
        return render(request, 'registration/login.html', context)

    def post(self, request):
        if request.POST.get('action', 'login') == 'login':
            return self.login_user(request)
        else:
            return self.register_user(request)

    def login_user(self, request):
        context = {}
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        context['login_form'] = form
        context['register_form'] = RegisterForm()
        return render(request, 'registration/login.html', context)

    def register_user(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password_1')
            user = User.objects.register_user(
                username, password,
                request, form.cleaned_data, settings.REGISTER_FIELDS)
            email = user.emails.first()
            if email:
                self.send_email(
                    email.email,
                    **{
                        'user': user,
                        'username': username,
                        'password': password
                    }
                )
            return HttpResponseRedirect('/')
        else:
            context = {'register_form': form, 'login_form': LoginForm(request)}
            return render(request, 'registration/login.html', context)

    def send_email(self, to_email, **kwargs):
        from mail.utils import send_email, render
        subject = render(self.mail_subject)
        html = render(
            self.mail_template, **kwargs
        )
        send_email(subject=subject, text=html, html=html, to=[to_email])


class LogoutView(View):
    methods = ['GET', 'POST']

    def logout_user(self, request):
        auth_logout(request)
        return HttpResponseRedirect('/')

    def get(self, request):
        return self.logout_user(request)

    def post(self, request):
        return self.logout_user(request)


# 4 views for password reset:
# - password_reset sends the mail


@csrf_protect
def password_reset(request,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=UserResetPasswordForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   extra_context=None,
                   html_email_template_name=None,
                   extra_email_context=None):
    """
    View from django witch changed for use email in konkord UserModel
    """
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
                'extra_email_context': extra_email_context,
            }
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class AccountView(MetaMixin, DetailView):
    methods = ['GET']
    model = User
    queryset = User.objects.active()
    template_name = 'users/account.html'

    def get_object(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return self.request.user
        raise Http404()

    def get_breadcrumbs(self):
        return [(_('Account'), ''), (_('Profile'), '')]


@method_decorator(login_required, name='dispatch')
class PasswordChangeView(MetaMixin, FormView):

    template_name = 'users/password_change.html'
    mail_template = 'users/password_change_mail.html'
    mail_subject = 'users/password_change_mail_subject.html'
    form_class = PasswordChangeForm

    def get_success_url(self):
        return reverse('users_password_change')

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        from django.contrib import messages
        form.save()
        to_email = self.request.user.email
        if to_email:
            self.send_email(to_email, **{'user': self.request.user})
        messages.success(self.request, _('Your password was changed'))
        return super(PasswordChangeView, self).form_valid(form)

    def send_email(self, to_email, **kwargs):
        from mail.utils import send_email, render
        subject = render(self.mail_subject)
        html = render(
            self.mail_template, **kwargs
        )
        send_email(subject=subject, text=html, html=html, to=[to_email])

    def get_breadcrumbs(self):
        return [(_('Account'), ''), (_('Password change'), '')]


class UserData(JSONResponseMixin, TemplateView):
    def get_data(self, context):
        data = {}
        user = self.request.user
        if user.is_authenticated():
            data['user_authenticated'] = True
            data['username'] = user.username
        else:
            data['authenticated'] = False
        return self.success_response(data)
