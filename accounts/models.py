from django.contrib.auth.models import AbstractUser,PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from domains.models import Domain




class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email,phone, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,phone,password, **extra_fields)

    def create_superuser(self, email,phone, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, phone,password, **extra_fields)
        


class CustomUser(AbstractUser,PermissionsMixin):
    
    email = models.EmailField(_('email address'), unique=True)
    phone = models.IntegerField(unique=True,null=True)
    username = models.CharField(max_length=244,null=True)
    is_client = models.BooleanField(default=False)
    is_expert = models.BooleanField(default=False)
    is_verified = models.CharField(max_length=100,default='true')
    is_block = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone','username']

    objects = CustomUserManager()

    
    
    def __str__(self):  
        return f'{self.username}' 
    


class Client(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    profile_poto = models.ImageField(upload_to='client/profile',null=True)
    address = models.CharField(max_length=255,null=True)
    wallet = models.IntegerField(null=True)
    

    def __str__(self):  
        return f'{self.user.username}' 
    




class Expert(models.Model):
    user = models.ForeignKey(CustomUser,related_name='expert',on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain,on_delete=models.CASCADE)
    profile_poto = models.ImageField(upload_to='expert/profile')
    certificate = models.ImageField(upload_to='expert/certificate')
    wallet = models.IntegerField(null=True)

    def __str__(self):  
        return f'{self.user.username}' 


   
    


