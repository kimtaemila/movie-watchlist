from django.test import TestCase
from myapp.models import Movie, Playlist, UserProfile, RequestMovie
from django.contrib.auth.models import User

import datetime


def create_movie(title, releasedate, language='en-US', description='N/A'):
    return Movie.objects.create(title=title,
                                releasedate=releasedate,
                                language=language,
                                description=description)


def create_user(username, password, **kwargs):
    user = User.objects.create(username=username,
                               password=password)
    user.first_name = kwargs['firstname']
    user.last_name = kwargs['lastname']
    user.email = kwargs['email']
    user.save()
    return user


def create_playlist(title, createdby, description='N/A'):
    return Playlist.objects.create(title=title,
                                   createdby=createdby,
                                   description=description)


def create_user_profile(user, is_paid):
    return UserProfile.objects.create(user=user, is_paid=is_paid)


def create_request(title, releasedate, requestedby, language='en-US', description='N/A'):
    return RequestMovie.objects.create(movietitle=title,
                                       releasedate=releasedate,
                                       language=language,
                                       requestedby=requestedby,
                                       )


class MovieTest(TestCase):

    def test_movie_creation(self):
        """
        Creates a Movie object
        """
        movie_released = create_movie(title='Released Test',
                                      releasedate=datetime.date(
                                          2016, 5, 13),
                                      )
        movie_not_released = create_movie(title='Not Released Test',
                                          releasedate=datetime.date(
                                              2021, 12, 31),
                                          )

        # SUCCESS TEST
        self.assertEquals(isinstance(movie_released, Movie), True)
        self.assertEquals(movie_released.__str__(),
                          f'{movie_released.releasedate.year} | {movie_released.title}')
        self.assertEquals(movie_released.is_released(), True)
        self.assertEquals(movie_not_released.is_released(), False)

        # FAIL TEST
        self.assertNotEquals(isinstance(movie_released, Movie), False)
        self.assertNotEquals(movie_released.is_released(), False)
        self.assertNotEquals(movie_not_released.is_released(), True)


class PlaylistTest(TestCase):

    def test_playlist_creation(self):
        """
        Creates a Playlist object
        """
        dummy_user = create_user(username='TestUser',
                                 password='user1234',
                                 firstname='Test',
                                 lastname='User',
                                 email='test.user@gmail.com')

        dummy_playlist = create_playlist(title='Dummylist',
                                         createdby=dummy_user)

        # SUCCESS TEST
        self.assertEquals(isinstance(dummy_playlist, Playlist), True)
        self.assertEquals(dummy_playlist.__str__(),
                          f'User: {dummy_playlist.createdby.username} | Title: {dummy_playlist.title}')

        # FAIL TEST
        self.assertNotEquals(isinstance(dummy_playlist, Playlist), False)


class UserprofileTest(TestCase):

    def test_userprofile_creation(self):
        """
        Creates a User Profile object
        """
        test_user1 = create_user(username='TestUser',
                                 password='user1234',
                                 firstname='Test',
                                 lastname='User',
                                 email='test.user1@gmail.com')
        test_user2 = create_user(username='TestUser2',
                                 password='user1234',
                                 firstname='Test',
                                 lastname='User2',
                                 email='test.user2@gmail.com')

        user_profile1 = create_user_profile(test_user1, False)
        user_profile2 = create_user_profile(test_user2, True)

        # SUCCESS TEST
        self.assertEquals(isinstance(test_user1, User), True)
        self.assertEquals(user_profile2.__str__(), user_profile2.user.username)
        self.assertEquals(user_profile2.is_paid, True)
        self.assertEquals(user_profile1.is_paid, False)

        # FAIL TEST
        self.assertNotEquals(isinstance(test_user1, User), False)
        self.assertNotEquals(user_profile2.is_paid, False)
        self.assertNotEquals(user_profile1.is_paid, True)


class RequestMovieTest(TestCase):

    def test_movie_request_creation(self):
        """
        Creates a Movie Request object
        """
        test_user1 = create_user(username='TestUser',
                                 password='user1234',
                                 firstname='Test',
                                 lastname='User',
                                 email='test.user1@gmail.com')

        movie_request1 = create_request(title='Request Test 1',
                                        releasedate=datetime.date(
                                            2021, 1, 1),
                                        requestedby=test_user1
                                        )

        # SUCCESS TEST
        self.assertEquals(isinstance(movie_request1, RequestMovie), True)
        self.assertEquals(movie_request1.__str__(),
                          f'{movie_request1.id} | {movie_request1.requestedby}')

        # FAIL TEST
        self.assertNotEquals(isinstance(movie_request1, RequestMovie), False)
