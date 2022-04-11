from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.

from online_shop.web.models import Profile, Product, Storage, Cart, Favorites

admin.site.site_header = 'BEST Parfume Shop Administration'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'age',)
    list_filter = ('gender',)


class StorageInlineAdmin(admin.StackedInline):
    model = Storage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (StorageInlineAdmin,)

    list_display = ('name', 'category', 'price',)


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity',)
    list_filter = ('user',)


@admin.register(Favorites)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product',)
    list_filter = ('user',)
