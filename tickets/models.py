from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User


class Movie(models.Model):
    name = models.CharField(max_length=50)
    hall = models.CharField(max_length=10)
    party = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.name


class Guest(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    class Meta:
        verbose_name = "Guest"
        verbose_name_plural = "Guests"

    def __str__(self):
        return self.name


class Reservation(models.Model):
    guest = models.ForeignKey(
        Guest, on_delete=models.CASCADE, related_name="reservation"
    )
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="reservation"
    )

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    def __str__(self):
        return str(self.id)


# auto create token to new user added
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def token_create(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


# permissions customization
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
