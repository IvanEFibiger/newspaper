from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"
    
    
class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    
    def __str__(self):
        return self.name
    
class Article(models.Model):
    title = models.CharField(max_length=250)
    lead = models.TextField(null=True)
    body = models.TextField()
    media = models.FileField(upload_to='media/', null=True, blank=True)
    media_footer = models.CharField(max_length=250, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_important = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']
    
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    article = models.ManyToManyField(Article)
    
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"



    

    
 