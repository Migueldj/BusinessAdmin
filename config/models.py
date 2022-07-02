from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password, **args):
        if not email:
            raise ValueError('Email is a required field')
        email = self.normalize_email(email)
        user = self.model(email=email, **args)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **args):
        args.setdefault('is_staff', True)
        args.setdefault('is_superuser', True)
        args.setdefault('is_active', True)

        return self.create_user(email, password, **args)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.pk is not None:
            if User.objects.get(pk=self.pk).password != getattr(self, 'password'):
                self.set_password(self.password)
        else:
            self.set_password(self.password)
        return super(User, self).save(*args, **kwargs)