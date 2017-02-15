from collections import OrderedDict
from .models import Rating
from catalog.settings import VARIANT, PRODUCT_WITH_VARIANTS
from django.contrib.contenttypes.models import ContentType
from .models import Review
from django.conf import settings
from catalog.models import Product


def product_variants(product):
    return product.variants.all()


def get_product_ids(product, exclude_variants=False):
    if product.product_type == PRODUCT_WITH_VARIANTS:
        ids = [product.id]
        if not exclude_variants:
            ids.extend(
                product_variants(product).values_list('id', flat=True))
    elif product.product_type == VARIANT:
        ids = [product.parent.id]
        ids.extend(
            product_variants(product.parent).values_list('id', flat=True))
    else:
        ids = [product.id]
    return ids


def get_reviews_qs(content_type_id, content_id, exclude_variants=False):
    is_product_model = ContentType.objects.filter(
        id=content_type_id, model=u'product').exists()
    if settings.REVIEWED_WITH_CHAINS_GROUP_REVIEWS_BY_PARENT_PRODUCT\
            and is_product_model:
        try:
            product = Product.objects.get(id=content_id)
        except:
            return []
        ids = get_product_ids(product, exclude_variants)
        return Review.objects.filter(
            content_type_id=content_type_id,
            content_id__in=ids,
            published=True,
            parent=None
        ).order_by('-create_date')
    else:
        return Review.objects.filter(
            content_type_id=content_type_id,
            content_id=content_id,
            published=True,
            parent=None
        ).order_by('-create_date')


def order_reviews_dict_by_rating(reviews_dict):
    from collections import OrderedDict
    return OrderedDict(sorted(
        reviews_dict.items(),
        key=lambda key: key[0].rating_yes - key[0].rating_no,
        reverse=True
    ))


def get_reviews_dict(
        content_type_id,
        content_id, group_by_parent=False, is_short_comment_filter=None,
        exclude_variants=False):
    is_product_model = ContentType.objects.filter(
        id=content_type_id, model=u'product').exists()
    if is_product_model and group_by_parent:
        try:
            product = Product.objects.get(id=content_id)
            ids = get_product_ids(product, exclude_variants)
        except:
            ids = []
    else:
        ids = [content_id]
    reviews = Review.objects.filter(
            content_type_id=content_type_id,
            content_id__in=ids,
            published=True,
            parent=None,
        ).order_by('-create_date')
    if is_short_comment_filter is not None:
        reviews = reviews.filter(is_short_comment=is_short_comment_filter)
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
        reviews_dict[review] = review.get_children().filter(published=True)
    if getattr(settings, 'REVIEWED_WITH_CHAINS_SORT_REVIEWS_BY_RATING', False):
        reviews_dict = order_reviews_dict_by_rating(reviews_dict)
    return reviews_dict
