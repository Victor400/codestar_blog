from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin 

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    
    list_display = ('title', 'slug', 'status')
    search_fields = ['title']
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

#admin.site.register(Post, PostAdmin)  # ✅ linked properly
admin.site.register(Comment)
