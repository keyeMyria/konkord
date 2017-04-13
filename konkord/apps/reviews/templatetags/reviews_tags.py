# coding: utf-8
from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from ..models import SCORE_CHOICES
from ..forms import ReviewForm
from ..utils import (
    order_reviews_dict_by_rating, get_reviews_qs
)

register = template.Library()


@register.inclusion_tag(
    'reviewed_with_chains/reviews_with_chains.html', takes_context=True)
def reviews_with_chains(
        context, obj, initial_insert=0,
        reviews_type='none', exclude_variants=False):
    content_type = ContentType.objects.get_for_model(obj)
    scores = []
    for i, score in enumerate(SCORE_CHOICES):
        scores.append({
            "title": str(score[0]),
            "value": str(score[0]),
            "z_index": 10-i,
            "width": (i+1) * 25,
        })
    return {
        'reviews_type': reviews_type,
        'review_form': ReviewForm(),
        'content_type_id': content_type.id,
        'content_id': obj.id,
        'scores': scores,
        'obj': obj,
        'initial_insert': initial_insert,
        'total_count': get_reviews_qs(content_type.id, obj.id).count(),
        'exclude_variants': exclude_variants,
    }


@register.simple_tag
def review_author_name(author):
    managers_group_name = \
        settings.REVIEWED_WITH_CHAINS_MANAGERS_GROUP_NAME
    if managers_group_name and author.user is not None and (
            author.user.groups.filter(name=managers_group_name).exists()
            or author.user.is_superuser):
        return settings.REVIEWED_WITH_CHAINS_MANAGERS_NAME
    else:
        return author.name


@register.inclusion_tag(
    'reviewed_with_chains/initial_all_reviews.html', takes_context=True)
def initial_all_reviews(context, content_type_id, content_id):
    from collections import OrderedDict
    from ..models import Rating
    from ..utils import get_reviews_qs
    reviews = get_reviews_qs(content_type_id, content_id)
    reviews_dict = OrderedDict()
    for review in reviews:
        review.rating_yes = Rating.objects.filter(
            review=review, rating=1).count()
        review.rating_no = Rating.objects.filter(
            review=review, rating=2).count()
        ratings = Rating.objects.filter(review=review).count()
        if ratings > 0:
            yes_count = Rating.objects.filter(
                review=review, rating=1).count()
            review.usefull = int(float(yes_count) / ratings * 100)
        reviews_dict[review] = review.get_children()
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
    return {
            'reviews': reviews_dict,
            'scores': scores,
            'content_type_id': content_type_id,
            'content_id': content_id,
    }


@register.inclusion_tag('reviewed_with_chains/average_rating.html')
def rwc_average_rating_for_instance(product):
    from ..utils import get_reviews_qs
    from django.db.models import Avg, Count
    content_type = ContentType.objects.get_for_model(product)
    rating_data = get_reviews_qs(content_type.id, product.id)\
        .filter(is_short_comment=False)\
        .aggregate(Avg('score'), Count('score'))
    return {
       'avg_score': rating_data['score__avg'],
       'reviews_count': rating_data['score__count']
    }


@register.inclusion_tag(
    'reviewed_with_chains/all_reviews.html', takes_context=True)
def initial_reviews_by_type(
        context,
        content_type_id,
        content_id, group_by_parent=0, reviews_type=None,
        exclude_variants=False):
    from ..utils import get_reviews_dict
    is_short_comment_filter = None
    if reviews_type == 'reviews':
        is_short_comment_filter = False
    elif reviews_type == 'short_comment':
        is_short_comment_filter = True
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
    return {
            'reviews': reviews_dict,
            'scores': scores,
            'content_type_id': content_type_id,
            'content_id': content_id,
    }
