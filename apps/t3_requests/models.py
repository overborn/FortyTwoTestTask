from django.db import models
from django.db.models import signals
from t8_tag.signals import model_log_handler


class Request(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=6)
    path = models.CharField(max_length=256)
    query = models.CharField(max_length=256, blank=True, null=True)
    priority = models.IntegerField(default=1)

    def __unicode__(self):
        return "[{0}] ({1}) {2}: {3} {4}".format(
            self.created.strftime('%Y-%m-%d %H:%M:%S'),
            self.priority,
            self.method,
            self.path,
            self.query
        )

signals.post_save.connect(model_log_handler)
signals.post_delete.connect(model_log_handler)
