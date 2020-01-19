from django.contrib import admin

from . models import TribalUser,Organisation, TribalSkills,Apply_tribal_to_org,Invite_tribal_to_org


admin.site.register(TribalUser)
admin.site.register(Organisation)
admin.site.register(TribalSkills)
admin.site.register(Apply_tribal_to_org)
admin.site.register(Invite_tribal_to_org)
# Register your models here.
