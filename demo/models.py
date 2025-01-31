from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email,full_name,phone_number=None, password=None, role='User', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not full_name:
            raise ValueError('THe Name field must be set')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            full_name = full_name,
            phone_number=phone_number or "",
            # role=role,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, phone_number=None, password=None, **extra_field):
        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_superuser', True)
        extra_field.setdefault('is_admin', True)
        # extra_field.setdefault('role','Admin')
        
        if extra_field.get('is_staff')is not True:
            raise ValueError('Superuser must have is_staff=True')
        
        if extra_field.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True')
        
        if extra_field.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        
        return self.create_user(
            email= email, 
            full_name=full_name,
            phone_number=phone_number,
            password = password, 
            **extra_field)
        
        

class User(AbstractBaseUser):
    
    username=None

    full_name=models.CharField(max_length=255)
    email= models.EmailField(unique=True)
    address= models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    is_superuser= models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)
    
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['full_name']
    
    objects=UserManager()
    
    def __str__(self):
        return f'{self.full_name}'
    
    def has_perm(self,perm,obj=None):
        if self.is_superuser:
            return True
            return False
    
    def has_module_perms(self, app_level):
        if self.is_superuser:
            return True
            return False
    
    

       
    
