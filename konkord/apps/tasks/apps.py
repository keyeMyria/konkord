from django.apps import AppConfig


class TasksConfig(AppConfig):
    name = 'tasks'

    def ready(self):
        from core import add_to_suit_config_menu
        from django.utils.translation import  ugettext_lazy as _
        add_to_suit_config_menu(
            'tasks',
            (
                {'url': 'rq_home', 'label': _('Django RQ')},
                {'model': 'tasks.job', 'label': _('Jobs')},
            )
        )