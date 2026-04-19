from django.contrib import admin

from blog.models import Topic, Profile, Article, Comment

# Register your models here
admin.site.register(Topic)
admin.site.register(Profile)
admin.site.register(Article)
admin.site.register(Comment)


