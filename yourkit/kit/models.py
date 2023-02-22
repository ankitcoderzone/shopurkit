from django.db import models

# Create your models here.
# from django.db import models
from django.contrib.auth.models import User

# Create your models here.
AREA_CHOICES=(
    ('Sidhari', 'Sidhari'),
    ('Narauli', 'Narauli'),
    ('Belaisa', 'Belaisa'),
    ('Chowk', 'Chowk'),
    ('Chhatavara', 'Chhatavara'),
    ('RTO', 'RTO'),
    ('Brahmashthan', 'Brahmashthan'),
)
CATEGORY_CHOICES=(
    ('CK', 'Cookies'),
    ('CH', 'Chocolates'),
    ('BF', 'Breakfast & instant food'),
    ('SM', 'Snacks & Munchies'),
    ('KI', 'Kitchen'),
    ('CD', 'Cold Drink'),
    ('DB', 'Dairy & Bread'),
    ('SS', 'Sauces & Spreads'),
    ('BS', 'Belaisa Store'),
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    
    product_image = models.FileField(upload_to='kit/images', default='')
    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    area = models.CharField(choices=AREA_CHOICES, max_length=100)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
   

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES=(
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('Delivered', 'Delivered'),
    ('Canceled', 'Canceled'),
    ('Pending', 'Pending'),
)
PAYMENT_CHOICES=(
    ('Online' , 'Online'),
    ('COD', 'COD'),

)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    amount = models.FloatField()
    payment = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='COD', null=True)
    # order = models.OneToOneField(OrderPlaced, on_delete=models.CASCADE)
#     # created_at =models.DateTimeField(auto_now_add=True, default=True)
#     # updated_at =models.DateTimeField(auto_now_add=True, default=True)
#     delivered= models.BooleanField(default=False)
   
   


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Accepted', null=True)

    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
