from django.db import models
from django.db.models import signals
from django_resized import ResizedImageField
from t8_tag.signals import model_log_handler


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField()
    skype = models.CharField(max_length=30)
    jabber = models.CharField(max_length=30, null=True, blank=True)
    other_contacts = models.TextField(null=True, blank=True)
    photo = ResizedImageField(
        size=[200, 200], upload_to='photo', null=True, blank=True)

    def __unicode__(self):
        return u"{0} {1}".format(self.first_name, self.last_name)


signals.post_save.connect(model_log_handler)
signals.post_delete.connect(model_log_handler)
