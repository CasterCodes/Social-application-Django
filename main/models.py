from django.db import models
import uuid
from datetime import datetime
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_bio = models.TextField(blank=True)
    user_profile_image =models.ImageField(upload_to='profiles', default='blank-profile-image.jpg')
    user_location = models.CharField(max_length=100,blank=True)

    def __str__(self) -> str:
        return self.user.username

class Post(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user  = models.CharField(max_length=100)
    image = models.ImageField(upload_to='posts')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    likes  = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user

class PostLikes(models.Model):
    post_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.username

class Following(models.Model):
    follower = models.CharField(max_length=255)
    user = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.user


