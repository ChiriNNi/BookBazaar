from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from books.models import Author


@receiver(post_save, sender=User)
def create_author(sender, instance, created, **kwargs):
    if created and instance.profile_type == 'author':
        Author.objects.create(first_name=instance.first_name, last_name=instance.last_name)