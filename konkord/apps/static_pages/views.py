# -*- coding: utf-8 -*-
from .models import PageCategory, Page
from django.shortcuts import render, get_object_or_404
from datetime import datetime,  timedelta
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie


def menu(request):
    categories = PageCategory.objects.filter(parent=None)
    return render(
        request, 'static_pages/menu.html', {'categories': categories})


def get_parent_template_news(category):
    if category.template_news == 'parent':
        return get_parent_template_news(category.parent)
    else:
        return category.template_news


def get_parent_template_category(category):
    if category.template_category == 'parent':
        return get_parent_template_category(category.parent)
    else:
        return category.template_category


@ensure_csrf_cookie
def view_category_or_news(request, category_slug, news_slug=''):
    categories = PageCategory.objects.filter(parent=None)
    category = get_object_or_404(PageCategory, slug=category_slug)
    template = None
    data = {}
    if news_slug:
        news = get_object_or_404(
            Page, slug=news_slug, category__slug=category_slug)
        if news.template != 'parent':
            template = 'static_pages/' + news.template
        else:
            pt = get_parent_template_news(category[0])
            template = 'static_pages/' + pt
        data = {
            'page_category': category,
            'page': news,
            'categories': categories,
            'info_page': True,
        }
    elif category:
        if category.template_category != 'parent':
            template = 'static_pages/' + category.template_category
        else:
            template = 'static_pages/' + get_parent_template_category(category)
        if category.sort == 1:
            category_news = list(category.page_set.filter(
                type=2,
                show_on_full_site=True
            ).exclude(
                active_date_stop__lte=datetime.today()
            ).exclude(
                active_date_start__gte=datetime.today() +
                timedelta(days=1)).order_by('-vip', 'position'))
            if settings.STATIC_PAGES_VIEW_CHILD_NEWS:
                category_news.extend(list(Page.objects.filter(
                    category__in=category.get_descendants(), type=2
                ).exclude(
                    active_date_stop__lte=datetime.today()
                ).exclude(
                    active_date_start__gte=datetime.today() +
                    timedelta(days=1)).order_by('-vip', 'position')))
        else:
            category_news = list(category.page_set.filter(
                type=2,
                show_on_full_site=True
            ).exclude(
                active_date_stop__lte=datetime.today()
            ).exclude(
                active_date_start__gte=datetime.today() +
                timedelta(days=1)).order_by('-vip', '-position'))
            if settings.STATIC_PAGES_VIEW_CHILD_NEWS:
                category_news.extend(list(Page.objects.filter(
                    category__in=category.get_descendants(),
                    type=2,
                    show_on_full_site=True,
                ).exclude(
                    active_date_stop__lte=datetime.today()
                ).exclude(
                    active_date_start__gte=datetime.today() +
                    timedelta(days=1)).order_by('-vip', '-position')))
        data = {
            'page_category': category,
            'current_slug': category_slug,
            'category': category,
            'category_slug': category_slug,
            'categories': categories,
            'category_news': category_news,
            'info_page': True,
        }
    return render(request, template, data)
