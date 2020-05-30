from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    body = models.TextField(max_length=1500, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_posts')
    publish = models.DateTimeField(default=timezone.now)
    #count of voices

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

############################
class Like(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='likes')

    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    #функция подсчета лайков

    class Meta:
        ordering = ('created',)