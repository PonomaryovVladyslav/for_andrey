from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView,
)

from blog.forms import ArticleForm, CommentForm
from blog.models import Article, Comment, Topic


class ArticleListView(ListView):
    """Главная страница: список всех статей (новые сверху)."""
    model = Article
    template_name = 'index.html'
    context_object_name = 'articles'


class MyFeedView(LoginRequiredMixin, ListView):
    """Лента статей по темам, на которые подписан пользователь."""
    template_name = 'my_feed.html'
    context_object_name = 'articles'

    def get_queryset(self):
        topics = self.request.user.subscribed_topics.all()
        return Article.objects.filter(topics__in=topics).distinct()


class ArticleDetailView(DetailView):
    """Детальная страница статьи с комментариями и формой комментария."""
    model = Article
    template_name = 'detail.html'
    pk_url_kwarg = 'article_id'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """Создание новой статьи."""
    model = Article
    form_class = ArticleForm
    template_name = 'article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AuthorRequiredMixin(UserPassesTestMixin):
    """Доступ к действию только автору статьи."""
    def test_func(self):
        return self.get_object().author == self.request.user


class ArticleUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """Редактирование статьи (только автор)."""
    model = Article
    form_class = ArticleForm
    template_name = 'article_form.html'
    pk_url_kwarg = 'article_id'


class ArticleDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """Удаление статьи (только автор)."""
    model = Article
    template_name = 'article_confirm_delete.html'
    pk_url_kwarg = 'article_id'
    success_url = reverse_lazy('home')


class CommentCreateView(LoginRequiredMixin, View):
    """Добавление комментария к статье."""
    def post(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            parent_id = request.POST.get('parent')
            if parent_id:
                comment.parent = Comment.objects.filter(pk=parent_id, article=article).first()
            comment.save()
        return redirect('article-detail', article_id=article.pk)


class TopicListView(ListView):
    """Список всех тем сайта."""
    model = Topic
    template_name = 'topics.html'
    context_object_name = 'topics'


class TopicDetailView(DetailView):
    """Все статьи по конкретной теме."""
    model = Topic
    template_name = 'topic_detail.html'
    pk_url_kwarg = 'topic_id'
    context_object_name = 'topic'


class TopicSubscribeView(LoginRequiredMixin, View):
    """Подписка на тему."""
    def post(self, request, topic_id):
        topic = get_object_or_404(Topic, pk=topic_id)
        topic.subscribers.add(request.user)
        return redirect(request.META.get('HTTP_REFERER') or topic.get_absolute_url())


class TopicUnsubscribeView(LoginRequiredMixin, View):
    """Отписка от темы."""
    def post(self, request, topic_id):
        topic = get_object_or_404(Topic, pk=topic_id)
        topic.subscribers.remove(request.user)
        return redirect(request.META.get('HTTP_REFERER') or topic.get_absolute_url())


class ProfileView(LoginRequiredMixin, TemplateView):
    """Профиль пользователя и список его подписок."""
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscribed_topics'] = self.request.user.subscribed_topics.all()
        return context


class RegisterView(CreateView):
    """Регистрация нового пользователя c автоматическим входом."""
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class BlogLoginView(LoginView):
    """Вход на сайт."""
    template_name = 'login.html'
    redirect_authenticated_user = True


class BlogLogoutView(LogoutView):
    """Выход с сайта."""
    next_page = reverse_lazy('home')


class SetPasswordView(PasswordChangeView):
    """Смена пароля (доступно только залогиненному пользователю)."""
    template_name = 'set_password.html'
    success_url = reverse_lazy('profile')


class ArticlesByMonthView(ListView):
    """Статьи, созданные в конкретный месяц."""
    template_name = 'articles_by_date.html'
    context_object_name = 'articles'

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        if not (1000 <= year <= 9999) or not (1 <= month <= 12):
            raise Http404('Некорректная дата')
        return Article.objects.filter(created_at__year=year, created_at__month=month)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']
        return context
