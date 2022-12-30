from django.urls import path
from . import views 



urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login,name='login'),
    path('logout', views.logout, name='logout'),
    path('account/settings', views.account_settings, name='account_settings'),
    path('upload/', views.upload_post, name='post_upload'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('like/', views.like, name='like'),
    path('follow/', views.follow, name='follow'),
    path('search/', views.search, name="search")
]