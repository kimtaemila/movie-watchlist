from django.contrib import admin
from .models import Playlist, Movie, UserProfile, RequestMovie

admin.site.register(Movie)
admin.site.register(Playlist)
admin.site.register(RequestMovie)
admin.site.register(UserProfile)
