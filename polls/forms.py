from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from users.models import CustomUser
from .models import Comment

class CommentForm(ModelForm):

    parent_comment_id = forms.IntegerField(
        widget = forms.HiddenInput, required=False)
    body = forms.CharField(
        label = '',
        widget = forms.Textarea
    )
    class Meta:
        model = Comment
        fields = ['body']
