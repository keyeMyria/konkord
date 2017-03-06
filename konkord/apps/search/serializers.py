# -*- coding: utf-8 -*-
from rest_framework import serializers
from catalog.models import Product


class LiveSearchSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'price', 'image', 'sale_price', 'retail_price', 'sale', 'url')

    def get_image(self, obj):
        image = obj.images.first()
        if image:
            return image.thumbnails['small']
        return ''

    def get_url(self, obj):
    	return obj.get_absolute_url()
  
