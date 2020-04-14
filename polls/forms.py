from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from users.models import CustomUser
from .models import Comment

class CommentForm(ModelForm):
    # url = forms.URLField(label='网址', required=False)
    # email = forms.EmailField(label='电子邮箱', required=True)
    login_user = forms.CharField(
        label='Логин',
        widget=forms.TextInput(
            attrs={
                'value': "",
                'size': "30",
                'maxlength': "245",
                'aria-required': 'true'}))
    parent_comment_id = forms.IntegerField(
        widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['body']
