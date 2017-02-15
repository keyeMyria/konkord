# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from adminconfig.utils import BaseConfig

MODERATE_MODE_CHOICES = (
    ('post_moderate', _('Post moderate')),
    ('pre_moderate', _('Pre moderate'))
)


class ReviewsConfigForm(forms.Form):
    max_reviews = forms.IntegerField(label=_('Max reviews'), initial=10)
    max_replies = forms.IntegerField(label=_('Max replies'), initial=10)
    moderate_mode = forms.ChoiceField(
        label=_('Moderate mode'), choices=MODERATE_MODE_CHOICES)
    group_reviews_by_parent_product = forms.BooleanField(
        label=_('Group reviews by parent product'),
        required=False
    )
    managers_group_name = forms.CharField(label=_('Managers group name'))


class ReviewsConfig(BaseConfig):
    form_class = ReviewsConfigForm
    block_name = 'reviews'
    name = _('Reviews')
    default_data = {
        'REVIEWED_WITH_CHAINS_MAX_REVIEWS': 10,
        'REVIEWED_WITH_CHAINS_MAX_REPLIES': 10,
        'REVIEWED_WITH_CHAINS_MODERATE_MODE': 'pre_moderate',
        'REVIEWED_WITH_CHAINS_GROUP_REVIEWS_BY_PARENT_PRODUCT': True,
        'REVIEWED_WITH_CHAINS_MANAGERS_GROUP_NAME': 'manager'
    }
    option_translation_table = (
        ('REVIEWED_WITH_CHAINS_MAX_REVIEWS', 'max_reviews'),
        ('REVIEWED_WITH_CHAINS_MAX_REPLIES', 'max_replies'),
        ('REVIEWED_WITH_CHAINS_MODERATE_MODE', 'moderate_mode'),
        (
            'REVIEWED_WITH_CHAINS_GROUP_REVIEWS_BY_PARENT_PRODUCT',
            'group_reviews_by_parent_product'),
        ('REVIEWED_WITH_CHAINS_MANAGERS_GROUP_NAME', 'managers_group_name'),
    )
