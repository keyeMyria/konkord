# -*- coding: utf-8 -*-
from django.db.models import ImageField


class ImageWithThumbnailsField(ImageField):
    def save(self, *args, **kwargs):
        super(ImageWithThumbnailsField, self).save(*args, **kwargs)
        import pdb; pdb.set_trace()