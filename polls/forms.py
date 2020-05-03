from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from users.models import CustomUser
from .models import Comment

class CommentForm(ModelForm):

    body = forms.CharField(
        label = '',
        widget = forms.Textarea(
                    attrs={
                        'class': 'comment-input',
                        'placeholder': 'Начните ввод...'
                    })
    )
    class Meta:
        model = Comment
        fields = ['body']
