from django.urls import path
from .views      import (
                            ProductListView,
                            ProductDetailsView,
                            Reviews,
                        )

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<product_id>', ProductDetailsView.as_view()),
    path('/<product_id>/review', Reviews.as_view())
]
