from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from users.models import CustomUser
from .models import Comment, Tag

class CommentForm(ModelForm):

    body = forms.CharField(
        label = '',
        widget = forms.Textarea(
                    attrs={
                        'class': 'comment-input',
                        'placeholder': 'Начните ввод...'
                    }))
    class Meta:
        model = Comment
        fields = ['body']

class TagForm(ModelForm):
    title = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'pass',
                                          'placeholder': 'Начните ввод...'}))
    tag_image = forms.ImageField(
            widget=forms.FileInput(attrs={'class': 'upload-image',
                                      'id': 'upload-image',
                                      'type': 'file',
                                      'name': 'pic[]'}),)
    def clean_title(self):
        title = self.cleaned_data['title'].lower()
        rs = Tag.objects.filter(title=title)
        if rs.count():
            raise ValidationError("Упс... Такая категория уже есть!")
        return title

    class Meta:
        model = Tag
        fields = ['title', 'tag_image']