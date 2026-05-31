from django import forms

from blog.models import Article, Comment


class ArticleForm(forms.ModelForm):
    """Форма создания и редактирования статьи."""
    class Meta:
        model = Article
        fields = ['title', 'content', 'topics']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'topics': forms.CheckboxSelectMultiple(),
        }


class CommentForm(forms.ModelForm):
    """Форма добавления комментария."""
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш комментарий...'}),
        }
        labels = {'text': 'Комментарий'}