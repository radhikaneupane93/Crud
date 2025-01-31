from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import BlogSerializer, UpdateSerializer, DeleteSerializer,CommentSerializer,LikeSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Blog,BlogComment,BlogLike
# Create your views here.


class BlogAPIView(APIView):
    
    # Create Blog 
    def post(self, request):
        try:
            serializer = BlogSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self,request, id=None):
        try:
            if id:
                blog = get_object_or_404(Blog, id=id)
                serializer = BlogSerializer(blog)
                return Response(serializer.data, status=status.HTTP_200_OK)
            blogs = Blog.objects.all()
            serializer = BlogSerializer(blogs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, id):
        try:
            blog = get_object_or_404(Blog, id=id)
            serializer = BlogSerializer(blog, data=request.data, partial= True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def delete(self, request, id):
        try:
            blog = get_object_or_404(Blog, id=id)
            
            blog.delete()
            return Response({"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class BlogCommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, blog_id):
        blog = get_object_or_404(Blog, id=blog_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(blog=blog, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, id=blog_id)
        comments = blog.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, blog_id):
        blog = get_object_or_404(Blog, id=blog_id)
        like, created = BlogLike.objects.get_or_create(blog=blog, user=request.user)

        if not created:
            return Response({"message": "You already liked this blog"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, blog_id):
        blog = get_object_or_404(Blog, id=blog_id)
        like = BlogLike.objects.filter(blog=blog, user=request.user)
        if like.exists():
            like.delete()
            return Response({"message": "Like removed"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "You have not liked this blog"}, status=status.HTTP_400_BAD_REQUEST)