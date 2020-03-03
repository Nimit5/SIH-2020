from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('', views.index,name="Index"),
    path('verifyotp', views.verifyotp,name="verifyotp"),
    path('login', views.login,name="login"),
    path('apply/<int:myid>', views.apply,name="apply"),
    path('uploadskill', views.uploadskill,name="uploadskill"),
    path('logout', views.logout,name="logout"),
    path('show_skill/<int:myid>', views.show_skill,name="show_skill"),
    path('show_profile', views.show_profile_tribal,name="show_profile_tribal"),
    path('register_org', views.registerorg,name="registerorg"),
    path('orgProfile', views.orgProfile,name="orgProfile"),
    path('contactorg', views.contactorg,name="contactorg"),
    path('makeapplication', views.makeapplication,name="makeapplication"),
    path('invite/<int:myid>/<str:myemail>', views.invite,name="invite"),
    path('makeinvitation', views.makeinvitation,name="makeinvitation"),
    path('myrequests', views.myrequests,name="myrequests"),
    path('invitations', views.invitation,name="invitation"),
    path('scheme', views.scheme,name="scheme"),
    path('viewrequest', views.viewrequest,name="viewrequest"),
    path('sendinvitationoforg', views.sendinvitationoforg,name="sendinvitationoforg"),
    path('viewskill', views.viewskill,name="viewskill"),
    path('rejectinvitation/<int:myid>',views.rejectinvitation,name="rejectinvitaion"),
    path('acceptinvitation/<int:myid>',views.acceptinvitation,name="acceptinvitaion"),
    path('rejectinvitationorg/<int:myid>',views.rejectinvitationorg,name="rejectinvitaionorg"),
    path('acceptinvitationorg/<int:myid>',views.acceptinvitationorg,name="acceptinvitaionorg"),
    path('viewprofileTribal/<str:myemail>',views.viewprofileTribal,name="viewprofileTribal"),
    path('viewrogprofile/<str:myemail>',views.viewrogprofile,name="viewrogprofile"),
]
if settings.DEBUG:
    urlpatterns =urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)