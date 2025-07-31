from django.views import generic
from .models import Post

class PostList(generic.ListView):
    #queryset = Post.objects.filter(status=1)  # Only show published posts
    model = Post  # not queryset=Post.objects.filter(...)
    template_name = "blog/index.html"
    paginate_by = 6
    context_object_name = "posts"  # <== This must match your template loop
    
    
