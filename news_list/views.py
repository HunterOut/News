from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from .forms import CommentForm, LikeForm, EmailPostForm
from django.core.mail import send_mail


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
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


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) порекомендовал вам статью "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Прочитайте "{}" по ссылке {}\n\n{} прокомментировал: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'knnews33@gmail.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'news_list/share.html', {'post': post,
                                                    'form': form, 'sent': sent})

