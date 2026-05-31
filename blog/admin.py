from django.contrib import admin

from blog.models import Topic, Profile, Article, Comment


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    filter_horizontal = ('subscribers',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'topics', 'created_at')
    search_fields = ('title', 'content')
    filter_horizontal = ('topics',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'created_at', 'parent')
    search_fields = ('text',)


admin.site.register(Profile)


