from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    name = 'reviews'

    def ready(self):
        from django.conf import settings
        from django.conf.urls import url, include
        from django.utils.translation import ugettext_lazy as _
        from core import add_to_suit_config_menu
        import reviews.listeners

        add_to_suit_config_menu(
            'users',
            (
                'reviews.Review',
                'reviews.Author'
            )
        )

        settings.APPS_URLS.append(
            url(r'^reviews/', include('reviews.urls'))
        )
        settings.REVIEWED_WITH_CHAINS_MAX_REVIEWS_EXCEEDED_ERROR =\
            _(u'Exceeded max reviews')
        settings.REVIEWED_WITH_CHAINS_MAX_REPLIES_EXCEEDED_ERROR =\
            _(u'Exceeded max replies')
        settings.REVIEWED_WITH_CHAINS_MANAGERS_NAME = _('Site manager')
