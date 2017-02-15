# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ''
    help = 'Project init'

    def handle(self, *args, **options):
        from django.contrib.sites.models import Site
        Site.objects.create(domain='example.com')
