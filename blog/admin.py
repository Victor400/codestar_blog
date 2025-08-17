from django.contrib import admin
from django.utils.timezone import localtime
from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on_display')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

    def created_on_display(self, obj):
        """Format created_on for display in admin."""
        return localtime(obj.created_on).strftime('%Y-%m-%d %H:%M')

    created_on_display.short_description = 'Created On'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'body', 'approved', 'created_on')
    list_filter = ('approved', 'created_on')
    search_fields = ('author__username', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        """Bulk approve selected comments."""
        queryset.update(approved=True)
