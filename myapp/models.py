from django.db import models
from django.core.exceptions import ValidationError
from django.utils.html import format_html

class User(models.Model):
    user_type_list = (
        ('buyer', 'buyer'),
        ('seller', 'seller'),
    )
    name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
    profile_image = models.ImageField(upload_to='user-images/', default='defaults/user-icon-1.png')
    user_type = models.CharField(
        max_length=10,
        choices=user_type_list,
        default='buyer'
    )

    def __str__(self):
        return self.name
    
class Product(models.Model):
    gender_type_list = (
        ('men', 'men'),
        ('women', 'women'),
        ('kids', 'kids'),
    )
    fashion_type_list = (
        ('professional', 'professional'),
        ('old_money', 'old_money'),
        ('wedding', 'wedding'),
    )

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "seller"},
        related_name="products"
    )

    company_name = models.CharField(max_length=100, default='Emerging-Company')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=9, decimal_places=2)    
    product_image = models.ImageField(upload_to='product-images/', default='defaults/user-icon-1.png')

    description = models.TextField()
    details = models.JSONField(default=dict, blank=True)
    available_no = models.PositiveIntegerField(default=0)
    
    gender_type = models.CharField(max_length=100, choices=gender_type_list, default='men')
    fashion_type = models.CharField(max_length=100, choices=fashion_type_list, default='professional')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['seller', 'name'],
                name='unique_seller_product'
            )
        ]

    def __str__(self):
        return f"{self.id} - {self.seller.name} - {self.name}"
    
    def clean(self):
        if self.seller.user_type != "seller":
            raise ValidationError({
                "seller": "Selected user is not a seller."
            })