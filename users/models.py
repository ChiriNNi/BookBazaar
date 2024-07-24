from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    PROFILE_CHOICES = (
        ('reader', 'Читатель'),
        ('author', 'Автор'),
    )
    image = models.ImageField(verbose_name='Аватарка', upload_to='users-images', null=True, blank=True)
    profile_type = models.CharField(max_length=10, choices=PROFILE_CHOICES, verbose_name='Profile Type',
                                    default='reader')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'