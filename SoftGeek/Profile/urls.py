from django.urls import path
from . import views




urlpatterns = [

    path('', views.profile, name='profile'),
    path('allProfiles/', views.ProfileListView.as_view(), name='all_profiles'),
    path('myInvites/', views.invites_received, name='my_invites'),
    path('myNetwork/', views.network_profiles_list, name='invites_profiles'),
    path('send_invits/', views.send_invitations, name='send_invits'),
    path('removeFriends/', views.remove_from_friends, name='remove_friends'),
    path('<slug>/', views.ProfileDetailView.as_view(), name='profile_detail_view'),
    path('invites/acceptInvitation/', views.accept_invitation, name='accept_invites'),
    path('invites/rejectInvitation/', views.reject_invitation, name='reject_invites'),
    
]