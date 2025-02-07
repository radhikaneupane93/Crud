from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer,UpdateSerializer,DeleteSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status,viewsets
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserApiView(APIView):
    
    # Create the data
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)     
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    
    # Read the data 
    def get(self, request, email=None):
        try: 
            if email:
                user = get_object_or_404(User, email=email)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    #Update
    def put(self,request,email):
        try:
            user = get_object_or_404(User, email=email)
            serializer =  UpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # Delete 
    def delete(self, request, email):
        try:
            user = get_object_or_404(User, email=email)
            serializer = DeleteSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            if serializer.validated_data['confirm']:
                user.delete()
                return Response({"message": "User Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Deletion not confirmed"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class LoginViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer 
    
    def create(self, request):
        try:
            serializer = self.serializer_class(data = request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data['email']
            password =  serializer.validated_data['password']
            
            user = User.objects.get(email=email)
            
            print("User", user)
            
            if user is None:
                return Response({"message": "Invalid credentail"}, status=status.HTTP_400_BAD_REQUEST)
            if not user.check_password(password):
                return Response({"message": "Invalid credentail"}, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            
            
            response_data = {
                "user_data": UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(access_token),
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e: 
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)           
        
        

def form(request):
    return render(request, "index.html")












        
# {
#     "full_name": "Radhika Neupane",
#     "email": "radhika@example.com",
#     "password": "password123",
#     "phone_number": "999999999"
# }
        

                    
        
        
    