# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
import logging

logger = logging.getLogger(__name__)


def model_log_handler(sender, instance, **kwargs):
    if (not settings.ENABLE_MODEL_LOGGING or
            sender._meta.object_name in settings.MODEL_LOG_IGNORE):
        return
    if 'created' in kwargs:
        action = ADDITION if kwargs.get('created') else CHANGE
    else:
        action = DELETION
    LogEntry.objects.log_action(
        user_id=1,
        content_type_id=ContentType.objects.get_for_model(instance).id,
        object_id=instance.id,
        object_repr=unicode(instance),
        action_flag=action
    )
    logger.info(LogEntry.objects.order_by('action_time').last())
