"""konkord URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^robots\.txt$', include('robots.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/', include('core.admin_urls')),
    url(r'^django-rq/', include('django_rq.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^favicon\.ico$', RedirectView.as_view(
        url=settings.STATIC_URL + 'img/fav.png')),
    url(r'^filer/', include('filer.urls')),
    url(
        r'^apple-touch-icon(?P<path>.*)$',
        RedirectView.as_view(
            url=settings.STATIC_URL + 'img/apple-touch-icons/apple-touch-icon%(path)s')
    ),
    url(r'^browserconfig\.xml$', RedirectView.as_view(
        url=settings.STATIC_URL + 'img/apple-touch-icons/browserconfig.xml')),
    url(
        r'^sitemap/(?P<path>.*)\.xml$',
        RedirectView.as_view(
            url='/sitemap.xml')
    ),
]
urlpatterns += i18n_patterns(
    url(r'^', include('core.urls')),
    prefix_default_language=False
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
