from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import BlogSerializer, UpdateSerializer, DeleteSerializer,CommentSerializer,LikeSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Blog,BlogComment,BlogLike
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
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
            serializer = UpdateSerializer(blog, data=request.data, partial= True)
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, id ):
        try:
            blog = Blog.objects.get(id=id)
            print(blog)
            comment = BlogComment.objects.create(
                blog=blog,
                user=request.user,
                comment_text = request.data['comment_text']   
            )
            serializer = CommentSerializer(comment)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Blog.DoesNotExist:
            return Response({"error":"Blog not found"}, status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response({"error":"Comment text is required"}, status=status.HTTP_400_BAD_REQUEST)
    
class BlogLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, id):
        try:
            blog = Blog.objects.get(id=id)
            blog_like, created = BlogLike.objects.get_or_create(blog=blog)

            if request.user in blog_like.likes.all():
                blog_like.likes.remove(request.user)
                return Response({"message": "Blog unliked."}, status=status.HTTP_200_OK)
            else:
                blog_like.likes.add(request.user)
                return Response({"message": "Blog liked."}, status=status.HTTP_201_CREATED)

        except Blog.DoesNotExist:
            return Response({"message": "Blog not found."}, status=status.HTTP_404_NOT_FOUND)

class BlogCommentListAPIView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes =[JWTAuthentication]
    
    def get(self, request, id):
        try:
            blog = Blog.objects.get(id=id)
            comments = BlogComment.objects.filter(blog=blog)
            serializer = CommentSerializer(comments, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
        
class BlogLikeListAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]

    def get(self, request, id):
        try:
            blog = Blog.objects.get(id=id)
            likes = BlogLike.objects.filter(blog=blog)
            print(likes)
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"error": "Blog not found."}, status=status.HTTP_404_NOT_FOUND)