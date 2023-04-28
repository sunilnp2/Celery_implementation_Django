from django.contrib import admin
from blog.models import Blog
# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'blog', 'add_by']
    list_display_links = ['id', 'title', 'blog', 'add_by']

admin.site.register(Blog,BlogAdmin)