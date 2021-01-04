from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from person.resources import PersonResource
from .models import Person

# Register your models here.


class PersonAdmin(ImportExportModelAdmin):
    resource_class = PersonResource


admin.site.register(Person, PersonAdmin)


# @admin.register(Person)
# class PersonAdmin(ImportExportModelAdmin):
#     pass
