from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Extend User model
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    address = models.TextField()
    sex = models.TextField()
    
    def __str__(self):
        return "%s's profile" % self.user
    
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile = UserProfile()
            profile.user = instance
            
    post_save.connect(create_user_profile, sender = User)