from django.db import models


class Request(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=6)
    path = models.CharField(max_length=256)
    query = models.CharField(max_length=256, blank=True, null=True)
    user = models.CharField(max_length=30, default='anonymous')

    def __unicode__(self):
        return u"{}: [{}] {}: {} {}".format(
            self.user,
            self.created.strftime('%Y-%m-%d %H:%M:%S'),
            self.method,
            self.path,
            self.query
        )
