from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')),
    path('store', include('store.urls')),
    path('order', include('order.urls')),
]
