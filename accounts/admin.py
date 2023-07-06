from django.contrib import admin
from .models import Customer, Product, Order, Tag
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'phone', 'email', 'date_created']


admin.site.register(Customer, CustomerAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'desc']


admin.site.register(Product, ProductAdmin)

admin.site.register(Tag)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'status']


admin.site.register(Order, OrderAdmin)
