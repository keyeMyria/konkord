from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from django.conf import settings
        from users.urls import urlpatterns
        from django.utils.translation import ugettext_lazy as _
        settings.APPS_URLS.extend(urlpatterns)
        settings.LOGIN_REDIRECT_URL = '/'
        settings.LOGIN_URL = '/login/'
        settings.REGISTER_FIELDS = (
            {
                'name': 'first_name',
                'class': 'CharField',
                'label': _(u'First name'),
                'required': False
            },
            {
                'name': 'last_name',
                'class': 'CharField',
                'label': _(u'Last name'),
                'required': False
            },
            {
                'name': 'phone',
                'class': 'CharField',
                'label': _(u'Telephone'),
                'required': True
            }
        )
        settings.AUTHENTICATE_BY = 'email'
