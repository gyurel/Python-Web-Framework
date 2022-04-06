from django.contrib import admin

# Register your models here.

from online_shop.web.models import Profile, Product, Storage, Cart


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'age',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price',)


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('quantity',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('quantity',)
