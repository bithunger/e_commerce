from . models import Product, ProductAttribute
from django.db.models import Min, Max

def filters(request):
    cat = Product.objects.distinct().values('category__title', 'category__id')
    brand = Product.objects.distinct().values('brand__title', 'brand__id')
    color = ProductAttribute.objects.distinct().values(
        'color__title', 'color__color_code', 'color__id')
    size = ProductAttribute.objects.distinct().values('size__title', 'size__id')
    minMax = ProductAttribute.objects.aggregate(Min('price'), Max('price'))
    
    data = {
        'cat': cat,
        'brand': brand,
        'color': color,
        'size': size,
        'minMax': minMax
    }
    
    return data