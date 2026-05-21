from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.PositiveIntegerField()
    password = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
