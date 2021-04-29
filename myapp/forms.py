from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Movie, Playlist, RequestMovie, UserProfile


class CreateMovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ('title',
                  'releasedate',
                  'slug',
                  'language',
                  'description',)


class CreatePlaylistForm(ModelForm):
    class Meta:
        model = Playlist
        fields = ('title',
                #   'slug',
                  'description',)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=32,
                                 required=False,
                                 help_text='Optional.')
    last_name = forms.CharField(max_length=32,
                                required=False,
                                help_text='Optional.')
    email = forms.EmailField(max_length=256,
                             help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'email',
                  'password1',
                  'password2',)


class RequestMovieForm(ModelForm):
    class Meta:
        model = RequestMovie
        fields = ('movietitle',
                  'releasedate',
                  'language',)


class PaymentForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('is_paid',)
