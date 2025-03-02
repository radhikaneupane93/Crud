from django.urls import path
from .views import *

urlpatterns = [
    path('blogCreation/', BlogCreation, name="BlogCreation"),
    path('blogInfo/', BlogInfo, name='BlogDetails' ),
    path('postUpdate/',PostUpdate, name='PostUpdate' ),
    
    path('blog/', BlogAPIView.as_view(), name='blog-list-create'),  
    path('blogdetails/', BlogAPIView.as_view(), name='blog-detail'), 
    
    path('blogs/<int:id>/comments/', BlogCommentAPIView.as_view(), name='blog-comment'),
    path('blogs/<int:id>/likes/', BlogLikeAPIView.as_view(), name='blog-like'),
    path('blogs/<int:id>/comments/list/', BlogCommentListAPIView.as_view(), name='blog-comments-list'),
    path('blogs/<int:id>/likes/list/', BlogLikeListAPIView.as_view(), name='blog-likes-list'),
]

