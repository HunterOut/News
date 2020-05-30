from django import forms
from .models import Comment, Like


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')


class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ('active',)
