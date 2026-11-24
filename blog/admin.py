from django.contrib import admin
from .models import (
    Bookmark,
    Reaction,
    Post,
    PostTag,
    Category,
    Tag,
)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    
    list_display = (
        "title",
        "author",
        "category",
        "status",
        "created_at",
    )

    list_filter = ("status", "category", "created_at")
    
    search_fields = ("title", "content", "author__username")
    
    prepopulated_fields = {"slug": ("title",)}


admin.site.register([
    Category,
    Tag,
    PostTag,
    Reaction,
    Bookmark,
])