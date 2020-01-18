from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('', views.index,name="Index"),
    path('verifyotp', views.verifyotp,name="verifyotp"),
    path('login', views.login,name="login"),
    path('apply', views.apply,name="apply"),
    path('uploadskill', views.uploadskill,name="uploadskill"),
    path('logout', views.logout,name="logout"),
    path('show_skill/<int:myid>', views.show_skill,name="show_skill"),
    path('show_profile', views.show_profile_tribal,name="show_profile_tribal"),
    path('register_org', views.registerorg,name="registerorg"),
    path('orgProfile', views.orgProfile,name="orgProfile"),
    path('contactorg', views.contactorg,name="contactorg"),
]
if settings.DEBUG:
    urlpatterns =urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)