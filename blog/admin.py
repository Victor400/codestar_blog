from django.contrib import admin
from .models import Post, Comment

admin.site.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Comment)
