from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from .forms import CommentForm, LikeForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'news_list/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    comments = post.comments.filter(active=True)
    new_comment = None

    likes = post.likes.filter(active=True)
    new_like = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    if request.method == 'POST':
        like_form = LikeForm(data=request.POST)
        if like_form.is_valid():
            new_like = like_form.save(commit=False)
            new_like.post = post
            new_like.save()
    else:
        like_form = LikeForm()

    return render(request, 'news_list/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'likes': likes,
                                                     'new_comment': new_comment,
                                                     'new_like': new_like,
                                                     'comment_form': comment_form,
                                                     'like_form': like_form,
                                                     })



