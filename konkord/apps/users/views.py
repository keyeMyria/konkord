# -*- coding: utf-8 -*-
from django.views.generic import View
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
    update_session_auth_hash
)
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import timezone
from django.utils.encoding import force_text
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
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
            from django.contrib.auth import login
            user = authenticate(username=username, password=password)
            login(request, user)
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
# - password_reset_done shows a success message for the above
# - password_reset_confirm checks the link the user clicked and
#   prompts for a new password
# - password_reset_complete shows a success message for the above

# @deprecate_current_app
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


# @deprecate_current_app
def password_reset_done(request,
                        template_name='registration/password_reset_done.html',
                        extra_context=None):
    context = {
        'title': _('Password reset sent'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
# @deprecate_current_app
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    # UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


# @deprecate_current_app
def password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
        'title': _('Password reset complete'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@sensitive_post_parameters()
@csrf_protect
@login_required
# @deprecate_current_app
def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@login_required
# @deprecate_current_app
def password_change_done(request,
                         template_name='registration/password_change_done.html',
                         extra_context=None):
    context = {
        'title': _('Password change successful'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)
