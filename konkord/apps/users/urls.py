# -*- coding: utf-8 -*-
from django.conf.urls import url
from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
    url(
        r'^password_reset/$',
        views.password_reset,
        name='user_password_reset'
    ),
    url(
        r'^password_reset/done/$',
        auth_views.password_reset_done,
        name='password_reset_done'
    ),
    url(
        r'^password_change/$',
        auth_views.password_change,
        name='password_change'
    ),
    url(
        r'^password_change/done/$',
        auth_views.password_change_done,
        name='password_change_done'
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(
        r'^reset/done/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'
    ),
    url(r'^account/$', views.AccountView.as_view(), name="account"),
    url(
        r'^account/password_change/$',
        views.PasswordChangeView.as_view(),
        name='users_password_change'
    ),
    url(
        r'^user-data/$',
        views.UserData.as_view(),
        name='user_data'
    )
]
