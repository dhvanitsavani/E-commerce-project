from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.PositiveIntegerField()
    password = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
    
class Seller(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.PositiveIntegerField()
    password = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    aadhar_card_no = models.PositiveBigIntegerField()
    address = models.TextField()