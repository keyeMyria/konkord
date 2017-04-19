# coding: utf-8
import json
import os
from django.conf import settings
import adminconfig
from django.core.exceptions import ImproperlyConfigured


class JSONConfigFile(object):
    """Implementation of project configuration based on JSON file.
    """
    def __init__(self, filename):
        self.filename = filename
        self.config = dict()

    def get_full_config(self):
        if os.path.exists(self.filename):
            self.config = json.load(open(self.filename, 'r'))
        else:
            self.config = dict()

    def save_full_config(self):
        json.dump(self.config, open(self.filename, 'w'))

    def get_block(self, name, default={}):
        self.get_full_config()
        result = default
        result.update(self.config.get(name, default))
        return result

    def set_block(self, name, data):
        self.get_full_config()
        self.config.update({name: data})
        self.save_full_config()


class BaseConfig(object):
    form_class = None
    block_name = 'default'
    default_data = dict()
    option_translation_table = tuple()

    def load_data(self):
        self.file_config = JSONConfigFile(
            filename=getattr(settings, 'GLOBAL_JSON_CONFIG', 'config.json'))
        self.config_block = self.file_config.get_block(
            self.get_block_name(), 
            default=self.default_settings()
            )

    def handle_files(self, files):
        from django.conf import settings
        import os
        media = settings.MEDIA_ROOT
        config_path = media + '/config/'
        if not os.path.exists(config_path):
            os.makedirs(config_path)
        media_root_dir = settings.MEDIA_ROOT
        if not media_root_dir.endswith('/'):
            media_root_dir += '/'
        for field_name, file in files.items():
            if not file:
                continue
            with open(config_path + file.name, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                self.config_block[self.field_name_to_option(field_name)] = {
                    'path': destination.name,
                    'url': settings.MEDIA_URL + destination.name.split(
                        media_root_dir)[-1]
                }


    def load_data_from_form(self, data):
        temp = self.field_names_to_options(data)
        self.config_block.update(temp)

    def save_data(self):
        self.file_config.set_block(
            self.get_block_name(), 
            self.config_block,
            )

    def get_block_name(self):
        return self.block_name

    def get_block(self):
        return self.config_block

    def option_to_field_name(self, option):
        for t in self.get_translation_table():
            if t[0] == option:
                return t[1]

    def field_name_to_option(self, field_name):
        for t in self.get_translation_table():
            if t[1] == field_name:
                return t[0]

    def options_to_field_names(self, data):
        result = dict()
        for t in data:
            result.update({
                self.option_to_field_name(t): data[t],
                })
        return result

    def field_names_to_options(self, data):
        result = dict()
        for t in data:
            result.update({
                self.field_name_to_option(t): data[t],
                })
        return result

    def get_translation_table(self):
        return self.option_translation_table

    def get_initial_data_for_form(self):
        return self.options_to_field_names(self.config_block)

    def get_form(self):
        return self.form_class

    def default_settings(self):
        return self.default_data


def restart_engine():
    """Restarting engine
    """
    from django.conf import settings
    import subprocess
    NGINX_RESTART_CODE = getattr(settings, 'NGINX_RESTART_CODE', False)
    if NGINX_RESTART_CODE:
        subprocess.call(NGINX_RESTART_CODE, shell=True)


def register(config):
    from django.conf import settings
    if not hasattr(config, 'block_name'):
        raise ImproperlyConfigured(str(config) + ' Has no attribute block_name')
    if not hasattr(config, 'name'):
        raise ImproperlyConfigured(str(config) + ' Has no attribute name')
    for config_name, config_value in config.default_data.items():
        setattr(settings, config_name, config_value)
    adminconfig.ADMIN_CONFIGURERS.append(
        (
            config.block_name,
            config.name,
            '.'.join([config.__module__, config.__qualname__])
        )
    )