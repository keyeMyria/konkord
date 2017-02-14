# -*- coding: utf-8 -*-
from rest_framework import serializers
from catalog.models import Product


class LiveSearchSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'price', 'image')

    def get_image(self, obj):
        image = obj.images.first()
        if image:
            return image.thumbnails['small']
        return ''
