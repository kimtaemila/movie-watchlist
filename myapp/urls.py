from django.urls import path, re_path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('requestmovie/', views.requestmovie, name='requestmovie'),
    path('createmovie/', views.createmovie, name='createmovie'),
    path('createlist/', views.createlist, name='createlist'),
    path('requests/', views.requests, name='requests'),
    path('profile/', views.userprofile, name='userprofile'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('search/', views.search_view, name='search'),
    path('donate/', views.donate, name='donate'),
    path('login/', views.login_view, name='login'),
    re_path(r'addtoplaylist/(?P<playlist_slug>[\w-]+)/(?P<movie_slug>[\w-]+)/$',
            views.addtoplaylist, name='addtoplaylist'),
    re_path(r'removefromplaylist/(?P<playlist_slug>[\w-]+)/(?P<movie_slug>[\w-]+)/$',
            views.removefromplaylist, name='removefromplaylist'),
    re_path(r'^movie/(?P<slug>[\w-]+)/$',
            views.moviedetails, name='moviedetails'),
    re_path(r'^playlist/(?P<slug>[\w-]+)/$',
            views.playlistdetails, name='playlistdetails'),
    path('', views.home, name='home'),
]
