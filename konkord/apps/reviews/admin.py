from django.contrib import admin
from .models import Author, Review, Rating
from genericadmin.admin import GenericAdminModelAdmin
from django.utils.translation import ugettext_lazy as _
from .forms import ReviewAdminForm, ReplyAdminAddForm
from django.contrib.admin import SimpleListFilter
from django.contrib.contenttypes.models import ContentType


class StatusFilter(SimpleListFilter):
    title = _('Review type')
    parameter_name = 'review_type'

    def lookups(self, request, model_admin):

        return (
            ('question', _(u'Question')),
            ('reviews', _(u'Review')),
            ('answer_the_question', _(u'Answer the question')),
            ('answer_the_review', _(u'Answer the review'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'question':
            return queryset.filter(
                is_short_comment=True, parent=None)
        elif self.value() == 'reviews':
            return queryset.filter(
                is_short_comment=False, parent=None)
        elif self.value() == 'answer_the_question':
            return queryset.filter(
                is_short_comment=True).exclude(parent=None)
        elif self.value() == 'answer_the_review':
            return queryset.filter(
                is_short_comment=False).exclude(parent=None)


class ReviewContentTypeFilter(SimpleListFilter):
    title = _('Review content type')
    parameter_name = 'review-content-type'

    def lookups(self, request, model_admin):
        content_types = ContentType.objects.filter(
            id__in=Review.objects.all().values('content_type').distinct()
        )
        return (
            (ct.id, ct.name)
            for ct in content_types
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(content_type__id=self.value())


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user')
    search_fields = ['name', 'email']

admin.site.register(Author, AuthorAdmin)


class ReviewAdmin(GenericAdminModelAdmin):

    form = ReviewAdminForm

    list_display = (
        'author',
        'score',
        'create_date',
        'content',
        'truncate_comment',
        'published',
        'parent_link',
    )
    change_form_template = 'admin/reviewed_with_chains_change_form.html'
    actions = ['moderate']
    ordering = ['-create_date']
    search_fields = ['author__name', 'content_id', 'comment']
    list_filter = (
        'score',
        'published',
        # StatusFilter,
        ReviewContentTypeFilter
    )

    def get_form(self, request, obj=None, *args, **kwargs):
        if 'admin_reply_add' in request.GET:
            return ReplyAdminAddForm
        else:
            return ReviewAdminForm

    def moderate(self, request, queryset):
        for review in queryset:
            review.published = True
            review.save()
    moderate.short_description = _('It has been moderated')

    def truncate_comment(self, obj):
        if len(obj.comment) > 50:
            return '%s...' % obj.comment[:50]
        else:
            return obj.comment
    truncate_comment.short_description = _('Comment')

    def parent_link(self, obj):
        if obj.parent is not None:
            return '<a href="/superadmin/reviewed_with_chains/review/%s/">%s</a>' % (
                obj.parent.id,
                obj.parent.author
                )
        else:
            return None

    parent_link.short_description = _('Parent review')
    parent_link.allow_tags = True


admin.site.register(Review, ReviewAdmin)

admin.site.register(Rating)
