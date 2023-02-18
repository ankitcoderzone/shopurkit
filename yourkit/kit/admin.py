from django.contrib import admin
from . models import *
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'area', 'zipcode','mobile']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(Payment)
class PaymentModeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'payment', 'customer']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id', 'user', 'customer', 'products', 'quantity', 'ordered_date', 'status']
    # def customers(self,obj):
    #     link=reverse('admin:app_customer_change',args=[obj.customer.pk])
    #     return format_html('<a href="{}">{}</a>',link,obj.customer.name)
    def products(self,obj):
        link=reverse('admin:kit_product_change',args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)
    # def users(self,obj):
    #     link=reverse('admin:app_user_change',args=[obj.user.pk])
    #     return format_html('<a href="{}">{}</a>',link,obj.user.name)

# Register your models here.


admin.site.site_header = "Login to urKIT"
admin.site.site_title = "Welcome to urKIT Dashboard"
admin.site.index_title = "urKIT Portal"
