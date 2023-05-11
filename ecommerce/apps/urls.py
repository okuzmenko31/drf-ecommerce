from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.users.urls')),
    path('categories/', include('apps.categories.urls')),
    path('products/', include('apps.products.urls')),
    path('basket/', include('apps.basket.urls')),
    path('orders/', include('apps.orders.urls')),
    path('stock/', include('apps.stock.urls'))
]
