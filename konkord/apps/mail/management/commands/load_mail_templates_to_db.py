# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.template.loaders.app_directories import get_app_template_dirs
from ...models import MailTemplate
import os


class Command(BaseCommand):
    args = ''
    help = 'Project init'

    def handle(self, *args, **options):
        template_dirs = get_app_template_dirs('templates')
        for template_dir in template_dirs:
            for dirname, dirnames, filenames in os.walk(template_dir):
                for filename in filenames:
                    if 'mail' in filename:
                        file_path = os.path.join(dirname, filename)
                        mail_template_name = file_path.split('templates/')[-1]
                        if os.path.exists(file_path):
                            MailTemplate.objects.get_or_create(
                                name=mail_template_name,
                                defaults={
                                    'html_template':
                                    open(file_path, 'r').read()
                                })
