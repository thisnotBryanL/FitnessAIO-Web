from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name ='profile')
    gender_choice = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    inches = models.IntegerField(default=0)
    feet = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=1000,decimal_places=1)
    calories = models.DecimalField(decimal_places=1, max_digits=10000, default=0)
    gender = models.CharField(max_length= 200, choices= gender_choice, default= 'Male')

    def __str__(self):
        return self.user.username

    def weight_float(self):
        return float(self.weight)

    def calories_float(self):
        return float(self.calories)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        post_save.connect(create_user_profile, sender='registration.Profile')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
