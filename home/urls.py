from django.urls import path
from . import views

app_name = 'home'  # Specify the namespace for your app's URLs

urlpatterns = [
    path('', views.home, name='home'),  # URL pattern for the 'home' view
    path('product/<str:product_id>/', views.product_detail, name='product_detail'),  # URL pattern for the 'product_detail' view
    path('category/<str:category_name>/', views.category, name='category'),

    # Add more URL patterns as needed for other views
]


