from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Topic(models.Model):
    """Тема/категория для статей"""
    name = models.CharField('Название', max_length=100)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    subscribers = models.ManyToManyField(
        User,
        related_name='subscribed_topics',
        blank=True,
    )

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('topic-detail', args=[self.pk])

    def __str__(self):
        return self.name


class Article(models.Model):
    """Статья блога"""
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        PUBLISHED = 'published', 'Опубликовано'
        ARCHIVED = 'archived', 'В архиве'

    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField('Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    topics = models.ManyToManyField(Topic, related_name='articles', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('article-detail', args=[self.pk])

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title, allow_unicode=True) or 'article'
            slug = base
            counter = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f'{base}-{counter}'
            self.slug = slug
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Комментарий к статье"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Комментарий от {self.author.username}'


class Profile(models.Model):
    """Профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return f'Профиль {self.user.username}'