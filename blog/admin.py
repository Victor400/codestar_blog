from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin 

from django.utils.timezone import localtime

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on_display')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

    def created_on_display(self, obj):
        return localtime(obj.created_on).strftime('%Y-%m-%d %H:%M')
    created_on_display.short_description = 'Created On'
