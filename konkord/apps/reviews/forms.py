from django import forms
from .models import Author, Review
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from catalog.models import Product
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class ReviewForm(forms.ModelForm):
    user_name = forms.CharField(
        label=pgettext_lazy('reviewed_with_chains', 'Name'))
    user_email = forms.EmailField(label=_('Email'))

    class Meta:
        model = Review
        exclude = ['author', 'content_type', 'content_id', 'create_date']

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['score'].localize = True
        self.fields['score'].initial = 5

    def clean(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get('is_short_comment', True)\
                and cleaned_data.get('score') is None:
            self.add_error('score', forms.ValidationError(_('Please rate this product')))
        return cleaned_data


class ReplyForm(forms.ModelForm):
    user_name = forms.CharField(
        label=pgettext_lazy('reviewed_with_chains', 'Name'))
    user_email = forms.EmailField(label=_('Email'))

    class Meta:
        model = Review
        fields = ['comment']
        exclude = ['create_date']


class ReviewAdminForm(forms.ModelForm):

    author_email = forms.CharField(label=_(u'Author email'), required=False)
    product = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'style': 'width:300px'}))

    class Meta:
        model = Review
        fields = [
            'published',
            'author',
            'author_email',
            'product',
            'comment',
            'score',
            'advantage',
            'cons',
            'content_type',
            'content_id',
            'create_date',
            'show_create_date',
            'parent',
            'is_short_comment',
            'receive_notifications'
        ]

    def __init__(self, *args, **kwargs):
        super(ReviewAdminForm, self).__init__(*args, **kwargs)

        if 'instance' in kwargs and self.instance.author:
            self.fields['author_email'].initial = self.instance.author.email
            self.fields['author_email'].widget.attrs['readonly'] = True
        if 'instance' in kwargs:
            p = Product.objects.filter(id=self.instance.content_id).first()
            self.fields['product'].initial = p.name if p else ''
            self.fields['product'].widget.attrs['readonly'] = True
            self.fields['product'].label = mark_safe(_(
                '<a href="%s">Product</a>') % reverse(
                    'admin:catalog_product_change', args=(
                        self.instance.content_id,)
                ))


class ReplyAdminAddForm(forms.ModelForm):

    product = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'style': 'width:300px'}))
    parent_text = forms.CharField(
        label=_('Parent text'),
        required=False,
        widget=forms.Textarea())

    class Meta:
        model = Review
        fields = [
            'published',
            'author',
            'product',
            'parent_text',
            'comment',
            'score',
            'content_type',
            'content_id',
            'parent',
        ]

    def __init__(self, *args, **kwargs):
        super(ReplyAdminAddForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs and 'admin_reply_add' in kwargs['initial']:
            from django.contrib.auth.models import User
            from django.conf import settings
            append_replies = getattr(
                settings,
                'REVIEWED_WITH_CHAINS_APPEND_REPLIES_TO_FIRST_LEVEL', False)
            user = User.objects.get(id=kwargs['initial']['user'])
            try:
                author = user.author_set.all()[0].id
            except:
                author = None
            review = Review.objects.get(id=kwargs['initial']['parent'])
            p = Product.objects.filter(id=review.content_id).first()
            self.fields['product'].initial = p.name if p else ''
            self.fields['product'].widget.attrs['readonly'] = True
            self.fields['product'].label = mark_safe(_(
                '<a href="%s">Product</a>') % reverse(
                    'admin:catalog_product_change', args=(
                        review.content_id,)
                ))
            self.fields['parent_text'].initial = review.get_root().comment\
                if append_replies else review.parent.comment
            self.fields['parent_text'].widget.attrs['readonly'] = True
            extra_intial = {
                'author': author,
                'content_id': review.content_id,
                'content_type': review.content_type,
                'published': True,
                'score': '',
            }
            if append_replies:
                extra_intial['parent'] = review.get_root().id
            self.initial.update(extra_intial)
