from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('products/', views.product, name='products'),
    path('product-details/<str:slug>/<int:id>', views.product_details, name='product-details'),
    path('categories/', views.category, name='categories'),
    path('category-products/<int:id>', views.category_products, name='category-products'),
    path('brands/', views.brands, name='brands'),
    path('brand-products/<int:id>', views.brand_products, name='brand-products'),
    path('filter-data', views.filter_data, name='filter-data'),
    path('load-more', views.load_more, name='load-more'),
    path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('cart-list/', views.cart_list, name='cart-list'),
    path('delete-cart-item/', views.delete_cart_item, name='delete-cart-item'),
    path('update-cart-item/', views.update_cart_item, name='update-cart-item'),
    path('accounts/signup', views.signup, name='signup'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('orders/', views.orders, name='orders'),
    path('orders-item/<int:id>', views.orders_item, name='orders_item'),
    
    path('add-to-wishlist/', views.add_wishlist, name='add_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('delete-wish-item/', views.delete_wish_item, name='delete_wish_item'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)