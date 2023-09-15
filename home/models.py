from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    USER_ROLES = [
        ('sotuvchi', 'Sotuvchi'),
        ('admin', 'Admin'),
        ('boshliq', 'Boshliq')
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=USER_ROLES)
    rating = models.FloatField()
    phone_nomber = models.CharField(max_length=20, blank=True)
    
    # class Meta:
    #     db_table = 'userprofile'

    def __str__(self) -> str:
        return self.user.get_full_name()
        
class Income(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    real_price = models.FloatField()
    time = models.DateField()
    p_amount = models.IntegerField(default=1)

    class Meta:
        db_table = 'income'

    def __str__(self) -> str:
        return str(self.product)
    

class Subcategory(models.Model):
    subcat = models.CharField(max_length=250)
    info = models.TextField()
    rating = models.FloatField(null=True)


    class Meta:
        db_table = 'subcategory'

    def __str__(self) -> str:
        return self.subcat
    
class Tipe(models.Model):
    tipe = models.CharField(max_length=100)
    info = models.TextField()
    rating = models.FloatField(null=True)

    class Meta:
        db_table = 'tipe'

    def __str__(self) -> str:
        return self.tipe
    


class Category(models.Model):
    category = models.CharField(max_length=100)
    info = models.TextField()
    rating = models.FloatField(null=True)

    class Meta:
        db_table = 'category'

    def __str__(self) -> str:
        return self.category
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Tipe, null=True,blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,null=True,blank=True, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,null=True,blank=True, on_delete=models.CASCADE)
    info = models.TextField(null=True)
    amount = models.IntegerField()
    price = models.FloatField()

    class Meta:
        db_table = 'product'

    def __str__(self) -> str:
        return self.name

