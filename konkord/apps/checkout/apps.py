from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    name = 'checkout'

    def ready(self):
        from django.conf import settings
        from django.utils.translation import ugettext_lazy as _
        from django.conf.urls import include, url
        import checkout.listeners
        settings.APPS_URLS.extend([
            url(r'^checkout/', include('checkout.urls'))
        ])
        settings.CHECKOUT_USER_FIELDS = (
            {
                'name': 'email',
                'class': 'EmailField',
                'label': _(u'Email'),
                'required': True
            },
            {
                'name': 'phone',
                'class': 'CharField',
                'label': _(u'Telephone'),
                'required': True
            },
            {
                'name': 'full_name',
                'class': 'CharField',
                'label': _(u'Full name'),
                'required': False
            },
        )