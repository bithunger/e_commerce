from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cat_imgs/')

    class Meta:
        verbose_name_plural = 'Categories'

    def img(self):
        return mark_safe('<img src="%s" width=50px; height: 50px />' % (self.image.url))

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brand_imgs/')

    def img(self):
        return mark_safe('<img src="%s" width=50px; height: 50px; />' % (self.image.url))

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=100)
    color_code = models.CharField(max_length=50)

    def color(self):
        return mark_safe('<div style="width: 42px; height: 15px; background-color:%s"></div>' % (self.color_code))

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=300)
    description = models.TextField()
    specific = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='prod_imgs/', null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.IntegerField()

    def img(self):
        return mark_safe('<img src="%s" width=50px; height: 50px />' % (self.image.url))

    def __str__(self):
        return self.product.title


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, default=None)
    email = models.CharField(max_length=150, default=None)
    mobile = models.CharField(max_length=20, default=None)
    address = models.CharField(max_length=100, default=None)
    total_amount = models.FloatField()
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    tran_id = models.CharField(max_length=150, default=None)

    class Meta:
        verbose_name_plural = 'Orders'


class OrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice = models.CharField(max_length=200)
    item = models.CharField(max_length=150)
    image = models.CharField(max_length=150)
    qty = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()

    def img(self):
        return mark_safe('<img src="/media/%s" width=50px; height: 50px />' % (self.image))

    class Meta:
        verbose_name_plural = 'Order items'


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
