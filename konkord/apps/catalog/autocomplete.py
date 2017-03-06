from dal import autocomplete
from . import models
from django.conf.urls import url


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = models.Product.objects.all()
        filter_sub_types = self.forwarded.get('filter_sub_types')
        exclude_slug = self.forwarded.get('exclude_slug')
        if filter_sub_types:
            qs = qs.filter(product_type__in=filter_sub_types)
        if exclude_slug:
            qs = qs.exclude(slug=exclude_slug)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class PropertyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = models.Property.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


urlpatterns = [
    url(
        r'^product-autocomplete/$',
        ProductAutocomplete.as_view(),
        name='product-autocomplete',
    ),
    url(
        r'^property-autocomplete/$',
        PropertyAutocomplete.as_view(),
        name='property-autocomplete',
    ),
]

