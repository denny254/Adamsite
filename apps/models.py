from django.db import models
import os 
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager,
    PermissionsMixin
    )
from django.db import models

class RegisterUserManager(BaseUserManager):

    def _create_user(self, email, password, first_name, last_name, phone_number, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        user = self.model(
            email=self.normalize_email(email), 
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, first_name, last_name, phone_number, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, first_name, last_name, phone_number, **extra_fields)

    def create_superuser(self, email, password,  first_name, last_name, phone_number, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))

        return self._create_user(email, password,  first_name, last_name, phone_number, **extra_fields)
    

    def get_by_natural_key(self, email):
        return self.get(email=email)
    


class RegisterUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects =  RegisterUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"



class Writers(models.Model):
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    date = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):   
        return self.name 
    
class Task(models.Model):
    STATUS_CHOICES = ( 
        ('New', 'New'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected'),
        ('Canceled', 'Canceled'),
        ('Revision', 'Revision'),
        ('Resubmition', 'Resubmition'),
        ('Pending', 'Pending'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    writer = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    book_balance = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()

    def __str__(self):
        return  f"{self.status} - {self.writer} - {self.client}"


class Project(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected'),
        ('Canceled', 'Canceled'),
        ('Revision', 'Revision'),
        ('Resubmission', 'Resubmission'),
        ('Pending', 'Pending'),
    )
    title = models.CharField(max_length=255)
    deadline = models.DateField()
    writer_assigned = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    attachment = models.FileField(blank=True, null=True, upload_to='images', default='avator.png')

    
    def __str__(self):
        return self.title
    
    def delete_old_file(self):
        if self.attachment:
            old_file = self.attachment.path 
    
            if os.path.isfile(old_file):
                os.remove(old_file) 

    def save(self, *args, **kwargs):
        self.delete_old_file()
        super().save(*args, **kwargs) 


        

    

