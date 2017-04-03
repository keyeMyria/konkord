from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from .models import Review, Author, Rating, SCORE_CHOICES
from .forms import ReviewForm, ReplyForm
from django.http import HttpResponse
import json
from django.template import RequestContext
from django.template.loader import render_to_string
from core.decorators import ajax_required
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .utils import (
    get_reviews_qs, get_product_ids, order_reviews_dict_by_rating, get_reviews_dict)
from catalog.models import Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage


@ajax_required
def add_review(request):
    data = {}
    json_data = {}
    if request.user.is_authenticated():
        user = request.user
        initial = {
            'user_name': user.first_name or user.username,
            'user_email': user.email,
        }
    else:
        initial = {}
    if request.POST:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            author, created = Author.objects.get_or_create(
                email=form.cleaned_data['user_email'])
            if created:
                author.name = form.cleaned_data['user_name']
            if request.user.is_authenticated():
                author.user = request.user
            author.save()
            managers_group_name = \
                settings.REVIEWED_WITH_CHAINS_MANAGERS_GROUP_NAME
            is_user_manager = request.user.groups.filter(
                    name=managers_group_name).exists()\
                or request.user.is_superuser
            is_product_model = ContentType.objects.filter(
                id=request.POST['content_type_id'], model=u'product').exists()
            if settings.REVIEWED_WITH_CHAINS_GROUP_REVIEWS_BY_PARENT_PRODUCT\
                    and is_product_model:
                try:
                    product = Product.objects.get(
                        id=request.POST['content_id'])
                    ids = get_product_ids(product)
                except:
                    ids = []
            else:
                ids = [request.POST['content_id']]
            reviews_count = author.review_set.filter(
                    content_id__in=ids).count()
            if managers_group_name and not is_user_manager and \
                    reviews_count >= settings.REVIEWED_WITH_CHAINS_MAX_REVIEWS:
                form._errors['__all__'] =\
                    [settings.REVIEWED_WITH_CHAINS_MAX_REVIEWS_EXCEEDED_ERROR]
                data['review_form'] = form
            else:
                review.author = author
                message = _(
                    u'Thank you, your review has adopted, he soon appear on the site.')
                if settings.REVIEWED_WITH_CHAINS_MODERATE_MODE ==\
                        'post_moderate' or is_user_manager:
                    message = _(
                        u'Thank you, your review has published.')
                    review.published = True
                review.content_type_id = request.POST['content_type_id']
                review.content_id = request.POST['content_id']
                review.save()
                data['review_form'] = ReviewForm(initial=initial)
                data['message'] = message
                json_data['added'] = True
        else:
            data['review_form'] = form
        data.update({
            'content_id': request.POST['content_id'],
            'content_type_id': request.POST['content_type_id'],
            'reviews_type': request.POST.get('reviews_type', None)
        })
    else:
        data['review_form'] = ReviewForm(initial=initial)
        data.update({
            'content_id': request.GET.get('content_id'),
            'content_type_id': request.GET.get('content_type_id'),
            'reviews_type': request.GET.get('reviews_type', None)
        })
    scores = []
    for i, score in enumerate(SCORE_CHOICES):
        scores.append({
            "title": str(score[0]),
            "value": str(score[0]),
            "z_index": 10-i,
            "width": (i+1) * 25,
        })
    data.update({
        'scores': scores,
    })
    html = render_to_string(
        "reviewed_with_chains/add_review_form.html",
        RequestContext(request, data)
    )
    json_data['html'] = html
    json_data['message'] = data['message'].capitalize()\
        if 'message' in data else None
    return HttpResponse(json.dumps(json_data))


@ajax_required
def all_reviews(request):
    from collections import OrderedDict
    content_type_id = request.POST.get('content_type_id', None)
    content_id = request.POST.get('content_id', None)
    review_id = request.POST.get('review_id', None)
    exclude_id = request.POST.get('exclude_id', None)
    page = request.POST.get('page', '1')
    total_count = 0
    if (not content_id or not content_type_id) and not review_id:
        return HttpResponse(json.dumps({'msg': ''}))
    reviews = None
    if review_id:
        reviews = Review.objects.filter(id=review_id)
    if not reviews:
        reviews = get_reviews_qs(content_type_id, content_id)
        if exclude_id:
            reviews = reviews.exclude(id=exclude_id)
    if reviews:
        reviews = reviews.annotate(created=F('create_date'))
    total_count += get_reviews_qs(content_type_id, content_id).count()
    paginator = Paginator(reviews, 3)
    try:
        current_page = paginator.page(int(page))
    except (EmptyPage, InvalidPage):
        current_page = paginator.page(paginator.num_pages)
    reviews_dict = OrderedDict()
    for review in current_page.object_list:
        review.is_review_with_chains = True
        review.rating_yes = Rating.objects.filter(
            review=review, rating=1).count()
        review.rating_no = Rating.objects.filter(
            review=review, rating=2).count()
        ratings = Rating.objects.filter(review=review).count()
        if ratings > 0:
            yes_count = Rating.objects.filter(
                review=review, rating=1).count()
            review.usefull = int(float(yes_count) / ratings * 100)
        reviews_dict[review] = review.get_children().filter(published=True)
    if getattr(settings, 'REVIEWED_WITH_CHAINS_SORT_REVIEWS_BY_RATING', False):
        reviews_dict = order_reviews_dict_by_rating(reviews_dict)
    scores = []
    for i, score in enumerate(SCORE_CHOICES):
        scores.append({
            "title": str(score[0]),
            "value": str(score[0]),
            "z_index": 10-i,
            "width": (i+1) * 25,
        })
    html = render_to_string(
        "reviewed_with_chains/all_reviews.html",
        RequestContext(
            request,
            {
                'reviews': reviews_dict,
                'scores': scores,
                'reply_form': ReplyForm(),
                'content_type_id': content_type_id,
                'content_id': content_id,
                'next_page': int(page) + 1
                if int(page) < paginator.num_pages else 1,
                'show_more_button': True if review_id else False,
                'exclude_id': (exclude_id or review_id) or '',
                'total_count': total_count,
            }
        )
    )
    return HttpResponse(json.dumps({'html': html}))


@ajax_required
def add_reply(request):
    data = {}
    json_data = {}
    if request.POST:
        form = ReplyForm(request.POST)
        if form.is_valid():
            review = Review.objects.get(id=request.POST['review_id'])
            reply = form.save(commit=False)
            author, created = Author.objects.get_or_create(
                email=form.cleaned_data['user_email'])
            if created:
                author.name = form.cleaned_data['user_name']
            if request.user.is_authenticated():
                author.user = request.user
            author.save()

            managers_group_name = \
                settings.REVIEWED_WITH_CHAINS_MANAGERS_GROUP_NAME
            replies_count = author.review_set.filter(
                    parent_id=request.POST['review_id']).count()
            is_user_manager = request.user.groups.filter(
                    name=managers_group_name).exists()\
                or request.user.is_superuser
            max_replies = settings.REVIEWED_WITH_CHAINS_MAX_REPLIES
            if managers_group_name and not is_user_manager and\
                    replies_count >= max_replies:
                form._errors['__all__'] = \
                    [settings.REVIEWED_WITH_CHAINS_MAX_REPLIES_EXCEEDED_ERROR]
                data['review_form'] = form
            else:
                reply.author = author
                message = _(
                    u'Thank you, your reply has adopted, he soon appear on the site.')
                if settings.REVIEWED_WITH_CHAINS_MODERATE_MODE ==\
                        'post_moderate' or is_user_manager:
                    reply.published = True
                    message = _(
                        u'Thank you, your reply has published.')
                reply.content_type_id = review.content_type_id
                reply.content_id = review.content_id
                reply.parent = review
                reply.save()
                data['review_form'] = None
                data['message'] = message
                json_data['added'] = True
        else:
            data['review_form'] = form
        data.update({
            'review_id': request.POST['review_id'],
            'reviews_type': request.POST.get('reviews_type', None)
        })
    else:
        if request.user.is_authenticated():
            user = request.user
            email = user.emails.filter(default=True).first()
            initial = {
                'user_name': user.first_name or user.username,
                'user_email': user.email,
            }
        else:
            initial = {}
        data['review_form'] = ReplyForm(initial=initial)
        data.update({
            'review_id': request.GET['review_id'],
            'reviews_type': request.POST.get('reviews_type', None)
        })
    html = render_to_string(
        "reviewed_with_chains/add_reply_form.html",
        RequestContext(request, data)
    )
    json_data['html'] = html
    json_data['message'] = data['message'].capitalize()\
        if 'message' in data else None
    return HttpResponse(json.dumps(json_data))


@ajax_required
def rating(request):
    review = Review.objects.get(id=request.POST['review_id'])
    rating = Rating.objects.get_or_create(
        review=review,
        user=request.user
    )[0]
    if request.POST['rating'] == 'yes':
        rating.rating = 1
    else:
        rating.rating = 2
    rating.save()
    data = {}
    yes_count = Rating.objects.filter(review=review, rating=1).count()
    no_count = Rating.objects.filter(review=review, rating=2).count()
    if yes_count > 0:
        data['yes'] = u'(%s)' % str(yes_count)
    else:
        data['yes'] = u''
    if no_count > 0:
        data['no'] = u'(%s)' % str(no_count)
    else:
        data['no'] = u''
    return HttpResponse(json.dumps(data))


@ajax_required
def all_reviews_by_type(request):
    content_type_id = request.POST.get('content_type_id', None)
    content_id = request.POST.get('content_id', None)
    group_by_parent = int(request.POST.get('group_by_parent', False))
    exclude_variants = int(request.POST.get('exclude_variants', 0)) == 1

    is_short_comment_filter = request.POST.get(
        'is_short_comment_filter', None)
    if is_short_comment_filter is not None:
        is_short_comment_filter = int(is_short_comment_filter)
    if not content_id or not content_type_id:
        return HttpResponse(json.dumps({'msg': ''}))
    reviews_dict = get_reviews_dict(
        content_type_id, content_id, group_by_parent, is_short_comment_filter,
        exclude_variants=exclude_variants)
    scores = []
    for i, score in enumerate(SCORE_CHOICES):
        scores.append({
            "title": str(score[0]),
            "value": str(score[0]),
            "z_index": 10-i,
            "width": (i+1) * 25,
        })
    html = render_to_string(
        "reviewed_with_chains/all_reviews.html",
        RequestContext(
            request,
            {
                'reviews': reviews_dict,
                'scores': scores,
                'reply_form': ReplyForm(),
                'content_type_id': content_type_id,
                'content_id': content_id,
                'short_comment_filter': is_short_comment_filter,
            }
        )
    )
    return HttpResponse(json.dumps({'html': html}))
