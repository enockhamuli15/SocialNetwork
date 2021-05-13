from django.urls import path
from . import views




urlpatterns = [

    path('', views.profile, name='profile'),
    path('myInvites/', views.invites_received, name='my_invites'),
    path('allProfiles/', views.ProfileListView.as_view(), name='all_profiles'),
    path('<slug>/', views.ProfileDetailView.as_view(), name='profile_detail_view'),
    path('toInviteProfile/', views.invites_profiles_list, name='invites_profiles'),
    path('send_invits/', views.send_invitations, name='send_invits'),
    path('removeFriends/', views.remove_from_friends, name='remove_friends'),
    path('acceptInvitation/', views.accept_invitation, name='accept_invites'),
    path('rejectInvitation/', views.reject_invitation, name='reject_invites'),
    
]