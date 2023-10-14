from django.urls import path,include
from . import views

app_name = 'home'  # Specify the namespace for your app's URLs

urlpatterns = [
    path('', views.home, name='home'),  # URL pattern for the 'home' view
    path('product/<str:product_id>/', views.product_detail, name='product_detail'),  # URL pattern for the 'product_detail' view
    path('category/<str:category_name>/', views.category, name='category'),
    path('discounts/', views.discounts, name='discounts'),
    path('chart/', views.chart, name='chart'),
    path('charts/', include('charts.urls')),


    # Add more URL patterns as needed for other views
]


