from django.contrib import admin
from t1_contact.models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'email')
    search_fields = ('first_name', 'last_name', 'date_of_birth', 'email')

admin.site.register(Person, PersonAdmin)
