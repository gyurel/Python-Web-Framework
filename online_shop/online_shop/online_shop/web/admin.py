from django.contrib import admin

# Register your models here.

from online_shop.web.models import Profile, Product, Storage, Cart, Favorites


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'age',)


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


@admin.register(Favorites)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product',)
