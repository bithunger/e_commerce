from django.contrib import admin
from .models import Category, Brand, Color, Size, Product, ProductAttribute, CartOrder, OrderItems, Wishlist


class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'img')
admin.site.register(Brand, BrandAdmin)


class ColorAdmin(admin.ModelAdmin):
    list_display = ('title', 'color')
admin.site.register(Color,ColorAdmin)

admin.site.register(Size)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'img')
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'brand', 'status', 'is_featured')
    list_editable = ('status', 'is_featured')
admin.site.register(Product, ProductAdmin)

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'img', 'product', 'price', 'color', 'size')
admin.site.register(ProductAttribute, ProductAttributeAdmin)

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'mobile', 'address', 'tran_id', 'total_amount', 'paid_status', 'order_date')
admin.site.register(CartOrder, CartOrderAdmin)

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'item', 'img', 'qty', 'price', 'total')
admin.site.register(OrderItems, OrderItemsAdmin)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
admin.site.register(Wishlist, WishlistAdmin)