from django.apps import AppConfig


class YasThemeConfig(AppConfig):
    name = 'yas_theme'

    def ready(self):
        from django.conf import settings
        from django.utils.translation import ugettext_lazy as _
        from yas_theme.urls import urlpatterns

        settings.REGISTER_FIELDS = (
            {
                'name': 'first_name',
                'class': 'CharField',
                'label': _('First name'),
                'required': False
            },
            {
                'name': 'last_name',
                'class': 'CharField',
                'label': _('Last name'),
                'required': False
            },
            {
                'name': 'phone',
                'class': 'CharField',
                'label': _('Telephone'),
                'required': True
            }
        )
        settings.CHECKOUT_USER_FIELDS = (
            {
                'name': 'email',
                'class': 'EmailField',
                'label': _(u'Your email'),
                'required': True
            },
            {
                'name': 'phone',
                'class': 'CharField',
                'label': _('Telephone'),
                'required': True
            },
            {
                'name': 'full_name',
                'class': 'CharField',
                'label': _('Recipient\'s name/company Name'),
                'required': True
            },
        )
        settings.USER_USERNAME_LABEL = _('Email address')
        settings.APPS_URLS.extend(urlpatterns)
        settings.MIDDLEWARE.append(
            'yas_theme.middleware.StartRedirectMiddleware')
