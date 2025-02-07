from rest_framework import serializers
from .models import Blog, BlogComment, BlogLike

class BlogSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'blog_title', 'blog_content', 'published_date', 'blog_author', 'comments', 'likes_count']

    def validate_blog_title(self, data):
        if len(data.strip()) < 5:
            raise serializers.ValidationError("Blog Title must be at least 5 characters long.")
        return data

    # Corrected method name to match 'comments' field
    def get_comments(self, obj):
        comments = BlogComment.objects.filter(blog=obj)  # Ensure BlogComment is related to Blog properly
        return CommentSerializer(comments, many=True).data  # Serialize comments

    def get_likes_count(self, obj):
        return obj.likes.count()  # Assuming Blog has a related `likes` manager

class UpdateSerializer(serializers.Serializer):
    class Meta:
        model = Blog
        fields = ['blog_title', 'blog_content']

    def update(self, instance, validated_data):
        instance.blog_title = validated_data.get('blog_title')
        instance.blog_content = validated_data.get('blog_content')
        instance.save()
        return instance

class DeleteSerializer(serializers.Serializer):
    confirm = serializers.BooleanField(required=True)

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = BlogComment
        fields = ['id', 'blog', 'user', 'comment_text', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogLike
        fields = ['id', 'blog', 'likes_count', 'created_at']
        
    def get_likes_count(self, obj):
        return obj.likes.count()
        

