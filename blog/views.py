from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import BlogPost, Comment, Like
from .forms import BlogPostForm, CommentForm, CustomUserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:  # Only the user who created the comment can delete it
        comment.delete()
    return redirect('about_us') 

def about_us(request):
    blog_posts = BlogPost.objects.all().order_by('-created_at')  # Newest posts first
    return render(request, 'blog/about_us.html', {'blog_posts': blog_posts})

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blog/blog_list.html', {'posts': posts})


def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'blog/blog_detail.html', {'post': post})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm
from .models import BlogPost

@login_required
def blog_post_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('about_us')  # Redirect to "About Us" page
    else:
        form = BlogPostForm()
    return render(request, 'blog/blog_post_form.html', {'form': form})

@login_required
def add_comment(request, post_pk):
    post = get_object_or_404(BlogPost, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            # Redirect to blog detail using reverse
            return HttpResponseRedirect(reverse('blog_detail', args=[post.pk]))
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form, 'post': post})


@login_required
def add_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            # Redirect back to the About Us page
            return redirect('about_us')
    # If not POST, redirect to About Us
    return redirect('about_us')


@login_required
def like_post(request, post_pk):
    post = get_object_or_404(BlogPost, pk=post_pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    # Redirect to blog detail using reverse
    return HttpResponseRedirect(reverse('blog_detail', args=[post.pk]))




def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after signup
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {'form': form})


def logout_view(request):
    logout(request)
    return redirect('blog_list')  # Redirect to blog list after logout
