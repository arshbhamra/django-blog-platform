from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q 
from django.conf import settings


class Category(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    desc = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="posts",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="posts",
        blank=True,
        null=True,
    )

    tags = models.ManyToManyField(
       Tag,
       through="PostTag",
       related_name="posts", 
       blank=True,
    )

    reacted_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Reaction",
        related_name="reacted_posts",
        blank=True,
    )
    
    bookmarked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Bookmark",
        related_name="bookmarked_posts",
        blank=True,
    )

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    content = models.TextField()
    
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering =  ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=~Q(status="published") | 
                Q(category__isnull=False),
                name="published_post_needs_category",
            ),
        ]
        
    def __str__(self):
        return self.title

class PostTag(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="tag_links",
    )

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="post_links",
    )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "tag"],
                name="unique_post_tag_pair",
            ),
        ]

    def __str__(self):
        return f"{self.post.title} - {self.tag.name}"
        
class Reaction(models.Model):
    
    class ReactionType(models.TextChoices):
        CLAP = "clap", "Clap"
        LOVE = "love", "Love"
        LIKE = "like", "Like"
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reactions",
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="reactions"
    )

    reaction_type = models.CharField(
        max_length=10,
        choices=ReactionType.choices,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
              fields=["user","post"],
              name="unqiue_user_post_reaction",
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.post} - {self.reaction_type}"
        
class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name = "bookmark_records",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_user_post_bookmark",
            ),
        ]

    def __str__(self):
        return f"{self.user} bookmarked {self.post}"