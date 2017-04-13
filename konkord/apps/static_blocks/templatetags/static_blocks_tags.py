# -*- coding: utf-8 -*-
from django.template import Library
from django.core.cache import cache
from django.utils import translation
from ..models import StaticBlock

register = Library()


@register.inclusion_tag(
    'static_blocks/static_block.html',
    takes_context=True)
def static_block(context, block_name):
    request = context.get('request')
    language = translation.get_language()
    cache_key = f'static-block-{block_name}-{language}'
    content = cache.get(cache_key)
    if content:
        return {'content': content}
    try:
        block = StaticBlock.objects.get(identifier=block_name)
        cache.set(cache_key, block.content)
        return {'content': block.content}
    except StaticBlock.DoesNotExist:
        return {
            'request': request,
            'block_name': block_name
        }
