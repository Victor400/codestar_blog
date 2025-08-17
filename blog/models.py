from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


def create_unique_slug(instance, title):
    """
    Generate a unique slug for a Post instance.
    """
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
    """
    Stores a single blog post entry related :model: 'User'
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    featured_image = CloudinaryField('image', default='placeholder')
    content = models.TextField(default='Placeholder content')
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']  # Newest posts appear first

    def save(self, *args, **kwargs):
        """Automatically generate a slug if not set."""
        if not self.slug:
            self.slug = create_unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} | written by {self.author}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='commenter'
    )
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}"
