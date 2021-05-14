from django.urls import path
from . import views
from Profile.views import profile
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login_page'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('passwordReset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('passwordResetDone/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('passwordResetConfirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('passwordResetComplete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('home/',  views.post_list_view, name='home_page'),
    path('home/comment/', views.post_comment_create_and_list_view, name='home_comment'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update', views.PostUpdateView.as_view(), name='post_update'),
    #path('home/', views.home1, name='home_page'),
    #path('home/', profile, name='profile'),
    path('likes/', views.blog_post_like, name="Likes"),
    path('domains/', views.domains, name='Alldomains'),
    path('notifications/', views.notifications, name='Allnotifications'),
    
]
