# -*- coding: utf-8 -*-
from django.contrib.postgres.fields import JSONField
from codemirror.widgets import CodeMirrorTextarea
import json


class UnicodeJSONField(JSONField):
    def formfield(self, **kwargs):
        kwargs['widget'] = CodeMirrorTextarea(
            mode='javascript',
            config={
                'fixedGutter': True,
                'lineWrapping': True,
            })
        return super(JSONField, self).formfield(**kwargs)

    def dumps_for_display(self, value):
        return json.dumps(
            value,
            indent=self.dump_kwargs.get("indent", 2)
        ).encode('utf8').decode('unicode_escape')
