from django.db import models
import os 

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


        

    
