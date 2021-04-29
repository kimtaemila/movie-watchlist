from django.contrib.auth.models import User
from django.db import models
from datetime import date

LANGUAGE_CHOICES = (
    ('ar-AE', 'Arabic (United Arab Emirates)'),
    ('bn-BD', 'Bengali (Bangladesh)'),
    ('bn-IN', 'Bengali (India)'),
    ('zh-CN', 'Chinese (China)'),
    ('en-US', 'English (United States)'),
    ('fr-FR', 'French (France)'),
    ('de-DE', 'German (Germany)'),
    ('hi', 'Hindi (India)'),
    ('id', 'Indonesian (Indonesia)'),
    ('ja', 'Japanese (Japan)'),
    ('ko-KR', 'Korean (South Korea)'),
    ('pt-PT', 'Portuguese (Portugal)'),
    ('es-ES', 'Spanish (Spain)'),
    ('ta-IN', 'Tamil (India)'),
    ('th', 'Thai (Thailand)'),
)


class Movie(models.Model):
    title = models.CharField(max_length=128,
                             blank=False,
                             verbose_name='Title')
    slug = models.SlugField(default='',
                            verbose_name='slug')
    m_type = models.CharField(max_length=32,
                              default='Movie',
                              verbose_name='Type')
    releasedate = models.DateField(blank=False,
                                   verbose_name='Release date')
    language = models.CharField(max_length=32,
                                default='en-US',
                                choices=LANGUAGE_CHOICES,
                                verbose_name='Language')
    description = models.TextField(blank=True)

    def __str__(self):
        year = self.releasedate.year
        return f'{year} | {self.title}'

    def is_released(self):
        now = date.today()

        if self.releasedate < now:
            return True

        return False


class Playlist(models.Model):
    title = models.CharField(max_length=32,
                             verbose_name='Title',)
    slug = models.SlugField(default='',
                            verbose_name='Slug',)
    p_type = models.CharField(max_length=32,
                              default='Playlist',
                              verbose_name='Type',)
    movies = models.ManyToManyField(Movie,
                                    blank=True,
                                    verbose_name='Movies',)
    createdby = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  verbose_name='Created by',)
    description = models.TextField(blank=True,
                                   max_length=512,
                                   verbose_name='Description')

    def __str__(self):
        return f'User: {self.createdby.username} | Title: {self.title}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False,
                                  help_text='Designates weather this user is premium',
                                  verbose_name='Premium')

    def __str__(self):
        return self.user.username


class RequestMovie(models.Model):
    movietitle = models.CharField(max_length=128,
                                  blank=False,
                                  verbose_name='Movie title')
    releasedate = models.DateField(blank=False,
                                   help_text='mm / dd / yyyy',
                                   verbose_name='Release date')
    language = models.CharField(max_length=32,
                                default='en-US',
                                choices=LANGUAGE_CHOICES,
                                verbose_name='Language')
    requestedby = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True,
                                    related_name='requested',
                                    verbose_name='Requested by')
    acceptedby = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   blank=True,
                                   null=True,
                                   related_name='accepted',
                                   verbose_name='Accepted by')
    accepted = models.BooleanField(default=False,
                                   help_text='Designates weather this request is acccepted.',
                                   verbose_name='Accepted')
    rejected = models.BooleanField(default=False,
                                   help_text='Designates weather this request is rejected.',
                                   verbose_name='Rejected')

    def __str__(self) -> str:
        return f'{self.id} | {self.requestedby}'
