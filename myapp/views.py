from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Playlist, Movie, UserProfile, RequestMovie
from . import forms
import re


# Custom decorators
def anonymous_required(function=None, redirect_url=None):
    """
        Decorator for views that checks that any user is not logged in, redirecting
        to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# def free_user_required(function=None, redirect_url=None):
#     """
#         Decorator for views that checks that any user is not logged in, redirecting
#         to the log-in page if necessary.
#     """
#     actual_decorator = user_passes_test(
#         lambda u: not u.userprofile.is_paid,
#         login_url=redirect_url,
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator


# Main views
def home(request):
    movies = Movie.objects.all().order_by('-releasedate__year', 'title')
    playlists = Playlist.objects.all().order_by('createdby', 'title')
    context = {
        'movies': movies,
        'playlists': playlists,
    }
    return render(request, 'myapp/collection.html', context)


def moviedetails(request, slug):
    movie = Movie.objects.all().get(slug=slug)
    playlists = Playlist.objects.filter(createdby=request.user.id)
    context = {
        'movie': movie,
        'playlists': playlists,
    }
    return render(request, 'myapp/moviedetails.html', context)


@anonymous_required(redirect_url='myapp:home')
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('myapp:home')
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})


@anonymous_required
def signup_view(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            userprofile = UserProfile(user=user)
            userprofile.save()
            #########################################################
            liked = Playlist(title='Liked', createdby=user,
                             slug=f'{user}-liked',
                             description='All the liked movies.')
            watched = Playlist(title='Watched', createdby=user,
                               slug=f'{user}-watched',
                               description='All the watched movies.')
            liked.save()
            watched.save()
            #########################################################
            login(request, user)
            return redirect('myapp:home')
    else:
        form = forms.SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})


def search_view(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        movies = Movie.objects.filter(title__contains=searched).order_by(
            '-releasedate__year', 'title')
        try:
            movies_date = Movie.objects.filter(
                releasedate__year=searched).order_by('-releasedate__year', 'title')
        except:
            movies_date = []

        context = {'searched': searched,
                   'movies': movies,
                   'movies_date': movies_date}
        return render(request, 'myapp/search.html', context=context)
    else:
        return render(request, 'myapp/search.html')


# FREE Users
@login_required(login_url='myapp:login')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('myapp:home')


@login_required(login_url='myapp:login')
def userprofile(request):
    playlists = Playlist.objects.filter(createdby=request.user.id)
    context = {
        'playlists': playlists,
    }
    return render(request, 'myapp/userprofile.html', context)


@login_required(login_url='myapp:login')
def playlistdetails(request, slug):
    playlist = Playlist.objects.all().get(slug=slug)
    all_movies = playlist.movies.all()
    context = {
        'playlist': playlist,
        'movies': all_movies,
    }
    return render(request, 'myapp/playlistdetails.html', context)


@login_required(login_url='myapp:login')
def donate(request):
    if request.method == 'POST':
        payment = request.POST.get('payment')
        if payment == 'paid':
            userprofile = request.user.userprofile
            userprofile.is_paid = True
            userprofile.save()

        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            return redirect('myapp:userprofile')
    return render(request, 'myapp/donate.html')


@login_required(login_url='myapp:login')
def addtoplaylist(request, playlist_slug, movie_slug):
    if request.method == 'POST':
        playlist = Playlist.objects.all().get(slug=playlist_slug)
        movie = Movie.objects.all().get(slug=movie_slug)
        playlist.movies.add(movie)
        return redirect('myapp:moviedetails', slug=movie_slug)


@login_required(login_url='myapp:login')
def removefromplaylist(request, playlist_slug, movie_slug):
    if request.method == 'POST':
        playlist = Playlist.objects.all().get(slug=playlist_slug)
        movie = Movie.objects.all().get(slug=movie_slug)
        playlist.movies.remove(movie)
        return redirect('myapp:playlistdetails', slug=playlist_slug)


# PREMIUM Users
@login_required(login_url='myapp:login')
def createlist(request):
    if request.method == 'POST':
        form = forms.CreatePlaylistForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.createdby = request.user
            instance.save()
            return redirect('myapp:home')
    else:
        form = forms.CreatePlaylistForm()

    return render(request, 'myapp/createlist.html', {'form': form})


@login_required(login_url='myapp:login')
def requests(request):
    if request.user.is_staff:
        requests = RequestMovie.objects.all().order_by('id')
        context = {'requests': requests, }

        if request.method == 'POST':
            action = request.POST.get('action')
            req_id = request.POST.get('request_id')
            req = RequestMovie.objects.filter(id=req_id)[0]

            if action == '✔️':
                title = req.movietitle
                date = req.releasedate
                f_title = re.sub(r'[\s\W-]+', '-',
                                 re.sub(r'&', '-and-', title.strip().lower()))
                slug = f'{str(date)[:4]}-{f_title}'
                lang = req.language
                newmovie = Movie(title=title,
                                 slug=slug,
                                 releasedate=date,
                                 language=lang)
                newmovie.save()
                req.accepted = True
                req.acceptedby = request.user
                req.save()

            elif action == '❌':
                req.delete()

            return redirect('myapp:requests')

        return render(request, 'myapp/requests.html', context=context)

    elif request.user.userprofile.is_paid:
        requests = RequestMovie.objects.filter(
            requestedby=request.user).order_by('id')
        context = {'requests': requests, }

        return render(request, 'myapp/requests.html', context=context)


@login_required(login_url='myapp:login')
def requestmovie(request):
    if request.method == 'POST':
        form = forms.RequestMovieForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.requestedby = request.user
            instance.save()
            return redirect('myapp:requestmovie')

    else:
        form = forms.RequestMovieForm()

    return render(request, 'myapp/requestmovie.html', {'form': form})


# ADMIN Users
@login_required(login_url='myapp:login')
def createmovie(request):
    if request.method == 'POST':
        form = forms.CreateMovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:createmovie')
    else:
        form = forms.CreateMovieForm()

    return render(request, 'myapp/createmovie.html', {'form': form})
