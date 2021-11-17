from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)

    token = models.FloatField(default=0)
    mining_time = models.IntegerField(default=0)

    # bool
    is_email_verified = models.BooleanField(default=False)

    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=12, blank=True, null=True)
    message = models.CharField(max_length=1024, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.username = self.user.username
        super(Chat, self).save(*args, **kwargs)
