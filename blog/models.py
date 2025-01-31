from django.db import models
from demo.models import User

# Create your models here.

class Blog(models.Model):
    blog_title = models.CharField(max_length=255)
    blog_content= models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    blog_author= models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.blog_title}'
    

class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment by {self.user.email} on {self.blog.blog_title}'
    
    
class BlogLike(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together=('blog','user')
        
    def __str__(self):
        return f'Liked by {self.user.email} on {self.blog.blog_title}'
    