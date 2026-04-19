# blog/views.py
from datetime import date

from django.http import HttpResponse
from django.shortcuts import render

from blog.models import Article


# blog/views.py
def home(request):
    # Пока у нас нет моделей, используем словари для имитации данных

    return render(request, 'index.html', {
        'site_name': 'Мой блог',
        'articles': Article.objects.all(),
        'topics': ['Python', 'Django', 'Web'],
        'today': date.today(),
    })

def about(request):
    return render(request, 'about.html')


def article_list(request):
    return HttpResponse("Список всех статей")


def article_detail(request, pk):
    return HttpResponse(f"Статья #{pk}")


def article_by_slug(request, slug):
    return HttpResponse(f"Статья: {slug}")

def articles_by_date(request, year, month, day):
    return HttpResponse(f"Статьи за {day}.{month}.{year}")

