from django.db import models
from django.utils.translation import ugettext_lazy as _, pgettext
from users.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from mptt.models import MPTTModel
from django.utils import timezone

SCORE_CHOICES = (
    (1, _(u"*")),
    (2, _(u"**")),
    (3, _(u"***")),
    (4, _(u"****")),
    (5, _(u"*****")),
)

RATING_CHOICES = (
    (1, _(u'yes')),
    (2, _(u'no'))
)


class Author(models.Model):
    name = models.CharField(
        verbose_name=pgettext('reviewed_with_chains', u'Name'),
        max_length=250,
        blank=True,
        null=True
    )
    email = models.EmailField(verbose_name=_(u'Email'))
    user = models.ForeignKey(
        User, verbose_name=_(u'User'), blank=True, null=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = _(u'Author')
        verbose_name_plural = _(u'Authors')


class Review(MPTTModel):
    published = models.BooleanField(
        verbose_name=_(u'Published'), default=False)
    author = models.ForeignKey(Author, verbose_name=_(u'Author'))
    comment = models.TextField(verbose_name=_(u'Comment'))
    score = models.IntegerField(
        pgettext('reviewed_with_chains', u"Score"),
        choices=SCORE_CHOICES,
        default=3,
        blank=True,
        null=True
    )
    advantage = models.TextField(
        verbose_name=_(u'Advantage'),
        blank=True,
        null=True
    )
    cons = models.TextField(verbose_name=_(u'Cons'), blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_(u"Content type")
    )
    content_id = models.PositiveIntegerField(
        _(u"Content ID"), blank=True, null=True)
    content = GenericForeignKey(
        ct_field="content_type", fk_field="content_id")
    create_date = models.DateTimeField(
        verbose_name=_(u'Create date'),
        default=timezone.now,
    )
    show_create_date = models.BooleanField(
        verbose_name=_(u'Show create date'),
        blank=True,
        default=True)
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        verbose_name=pgettext('reviewed_with_chains', u"Parent")
    )
    is_short_comment = models.BooleanField(
        verbose_name=_('Short comment'),
        default=False
    )

    receive_notifications = models.BooleanField(
        verbose_name=_(u'Receive notifications'),
        default=False,
        blank=True)

    def __str__(self):
        return u'%s' % self.author.name

    class Meta:
        verbose_name = _(u'Review')
        verbose_name_plural = _(u'Product reviews')

    def save(self, ignore_parent_save=False, *args, **kwargs):
        if self.parent is not None and not\
                self.parent.published and not ignore_parent_save:
            parent = self.parent
            parent.published = True
            parent.save(ignore_parent_save=True)
        super(Review, self).save(*args, **kwargs)


class Rating(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'User'))
    review = models.ForeignKey(Review, verbose_name=_(u'Review'))
    rating = models.IntegerField(
        _(u'Rating'),
        choices=RATING_CHOICES,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _(u'Rating')
        verbose_name_plural = _(u'Ratings')
