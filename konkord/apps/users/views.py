# -*- coding: utf-8 -*-
from django.views.generic import View
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
)
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import timezone
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from users.forms import RegisterForm, LoginForm, UserResetPasswordForm
from users.models import User, Email, Phone


class LoginView(View):
    def get(self, request):
        context = {}
        context['login_form'] = LoginForm(request)
        context['register_form'] = RegisterForm()
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
            now = timezone.now()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password_1')
            user_data = {
                'username': username,
                'is_staff': False,
                'is_active': True,
                'is_superuser': False,
                'last_login': now,
                'date_joined': now,
                'extra_data': {}
            }
            phone = None
            email = None
            for field in settings.REGISTER_FIELDS:
                value = form.cleaned_data.get(field['name'])
                if value:
                    if field['name'] in ['first_name', 'last_name']:
                        user_data[field['name']] = value
                    elif field['name'] == 'phone':
                        phone = value
                    elif field['name'] == 'email':
                        email = value
                    else:
                        user_data['extra_data'][field['name']] = value
            user = User(**user_data)
            user.set_password(password)
            user.save()
            auth_by = getattr(settings, 'AUTHENTICATE_BY', 'email')
            if auth_by == 'email':
                Email.objects.create(
                    email=user.username, default=True, user=user)
            else:
                Phone.objects.create(
                    number=user.username, default=True, user=user)
            if phone:
                if auth_by == 'phone' and phone != user.username:
                    Phone.objects.create(
                        number=phone, default=False, user=user)
                elif auth_by != 'phone':
                    Phone.objects.create(
                        number=phone, default=True, user=user)
            if email:
                if auth_by == 'email' and email != user.username:
                    Email.objects.create(
                        email=email, default=False, user=user)
                elif auth_by != 'email':
                    Email.objects.create(
                        email=email, default=True, user=user)
            from django.contrib.auth import authenticate
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return HttpResponseRedirect('/')
        else:
            context = {}
            context['register_form'] = form
            context['login_form'] = LoginForm(request)
            return render(request, 'registration/login.html', context)


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
