from django.views import generic
from .models import Post

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)  # Only show published posts
    template_name = "blog/post_list.html"
    context_object_name = "posts"  # <== This must match your template loop
    
