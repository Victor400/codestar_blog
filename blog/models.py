from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

def create_unique_slug(instance, title):
    slug = slugify(title)
    cls = instance.__class__
    count = 1
    unique_slug = slug

    while cls.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{count}"
        count += 1

    return unique_slug

STATUS = ((0, "Draft"), (1, "Published"))

class Post(models.Model):
    title       = models.CharField(max_length=200, unique=True)
    slug        = models.SlugField(max_length=200, unique=True)
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    excerpt     = models.TextField(blank=True)
    updated_on  = models.DateTimeField(auto_now=True)
    content     = models.TextField(default='Placeholder content')
    created_on  = models.DateTimeField(auto_now_add=True)
    status      = models.IntegerField(choices=STATUS, default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
