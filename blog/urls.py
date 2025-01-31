from django.urls import path
from .views import BlogAPIView,BlogCommentAPIView,BlogLikeAPIView

urlpatterns = [
    path('blog/', BlogAPIView.as_view(), name='blog-list-create'),  
    path('blog/<int:id>/', BlogAPIView.as_view(), name='blog-detail'), 
    path('blogs/<int:blog_id>/comments/', BlogCommentAPIView.as_view(), name='blog-comments'),
    path('blogs/<int:blog_id>/comments/', BlogLikeAPIView.as_view(), name='blog-comments'),
]