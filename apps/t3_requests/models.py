from django.db import models


class Request(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=6)
    path = models.CharField(max_length=256)
    query = models.CharField(max_length=256)

    def __unicode__(self):
        return "[{0}] {1}: {2} {3}".format(
            self.created.strftime('%Y-%m-%d %H:%M:%S'),
            self.method,
            self.path,
            self.query
            )
