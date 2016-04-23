# -*- coding: utf-8 -*-
from django.conf import settings
from t8_tag.models import ModelLogEntry


def model_log_handler(sender, **kwargs):
    if (not settings.ENABLE_MODEL_LOGGING or
            sender._meta.object_name == 'ModelLogEntry'):
        return
    if 'created' in kwargs:
        action = "CREATE" if kwargs.get('created') else "UPDATE"
    else:
        action = "DELETE"
    entry = ModelLogEntry(
        model=sender._meta.object_name,
        instance=kwargs.get('instance'),
        action=action
    )
    entry.save()
