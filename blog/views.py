from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic

from .forms import CommentForm
from .models import Comment, Post


class PostList(generic.ListView):
    """List view for published posts."""
    model = Post
    template_name = "blog/index.html"
    paginate_by = 6
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(status=1)


def post_detail(request, slug):
    """
    Display an individual blog post with its comments.
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = comments.count()
    comment_form = CommentForm()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment submitted, awaiting approval")
            return redirect("post_detail", slug=slug)

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )


def profile_page(request):
    """
    User profile page with their comments.
    """
    user = get_object_or_404(User, pk=request.user.id)
    comments = user.commenter.all()
    return render(
        request,
        "blog/profile.html",
        {"user": user, "comments": comments},
    )


def comment_edit(request, slug, comment_id):
    """
    View to edit comments.
    """
    if request.method == "POST":
        post = get_object_or_404(Post, status=1, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.success(request, "Comment updated!")
        else:
            messages.error(request, "Error updating comment!")

    return HttpResponseRedirect(reverse("post_detail", args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    View to delete comments.
    """
    post = get_object_or_404(Post, status=1, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.success(request, "Comment deleted!")
    else:
        messages.error(request, "You can only delete your own comments!")

    return HttpResponseRedirect(reverse("post_detail", args=[slug]))
