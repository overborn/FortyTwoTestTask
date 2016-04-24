from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField()
    skype = models.CharField(max_length=30)
    jabber = models.CharField(max_length=30, null=True, blank=True)
    other_contacts = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{} {} {} {}".format(
            self.first_name, self.last_name, self.date_of_birth, self.email)
