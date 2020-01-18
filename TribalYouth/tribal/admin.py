from django.contrib import admin

from . models import TribalUser,Organisation, TribalSkills


admin.site.register(TribalUser)
admin.site.register(Organisation)
admin.site.register(TribalSkills)
# Register your models here.
