from django.contrib import admin

from . models import UserProfile,Post,PostLikes, Following

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(PostLikes)
admin.site.register(Following)
