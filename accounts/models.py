from django.db import models

class Writers(models.Model):
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    date = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
