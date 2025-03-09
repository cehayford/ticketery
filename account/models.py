from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
import os
from uuid import uuid4

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('Password is required')
        
        user = self.model(
            email = self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        try:
            user = self.create_user(
                email= email,
                password=password,
                **extra_fields
            )
            return user
        except:
            raise ValueError('An Error Occured Please Try Again')


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    username = models.CharField(max_length=255)
    groups = None
    user_permissions = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        User.username = self.first_name + " " + self.last_name
        return f"{self.first_name} {self.last_name} {self.email} {self.username}"


class UserInfo(models.Model):
    userid = models.UUIDField(verbose_name='UserId', default=uuid4, editable=False)
    first_name = models.ForeignKey(User.first_name, related_name='first_name', on_delete=models.CASCADE)
    last_name = models.ForeignKey(User.last_name, related_name='last_name', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    user_address = models.TextField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        User.username = self.first_name + " " + self.last_name
        return User.username
    
    def delete(self, *args, **kwargs):
        # Delete image files associated with image fields
        image_fields = [field for field in self._meta.fields if isinstance(field, models.ImageField)]
        for field in image_fields:
            file_path = getattr(self, field.name).path
            print(file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
        super().delete(*args, **kwargs)


class BookingHistory(models.Model):
    user = models.OneToOneField
    payment_methods = models.JSONField(blank=True, null=True)
    event_preferences = models.JSONField(default=dict)
    membership_status = models.CharField(max_length=50, blank=True, null=True)
    subscription_details = models.JSONField(blank=True, null=True)
    two_factor_enabled = models.BooleanField(default=False)
    recent_login_activity = models.JSONField(default=list, blank=True)
