from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post

class PostList(generic.ListView):
    #queryset = Post.objects.filter(status=1)  # Only show published posts
    model = Post  # not queryset=Post.objects.filter(...)
    template_name = "blog/index.html"
    paginate_by = 6
    context_object_name = "posts"  # <== This must match your template loop

    from django.shortcuts import render, get_object_or_404  # ✅ Step 6

def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "blog/post_detail.html",
        {"post": post},
    )

    
    
