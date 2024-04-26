from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

class Album(models.Model):
    artist = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    release_date = models.DateField()  # Use DateField to store the release date
    format = models.CharField(max_length=50)
    label = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    review = 'test'
    def __str__(self):
        return f"{self.artist} - {self.title}"

class Review(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='reviews')
    metacritic_critic_score = models.IntegerField()
    metacritic_reviews = models.IntegerField()
    metacritic_user_score = models.DecimalField(max_digits=3, decimal_places=1)
    metacritic_user_reviews = models.IntegerField()

    def __str__(self):
        return f"{self.album.title} Metacritic Review"

class Aoty(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='aoty_reviews')
    aoty_critic_score = models.IntegerField()
    aoty_critic_reviews = models.IntegerField()
    aoty_user_score = models.DecimalField(max_digits=3, decimal_places=1)
    aoty_user_reviews = models.IntegerField()

    def __str__(self):
        return f"{self.album.title} AOTY Review"

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.album} ({self.quantity})"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
