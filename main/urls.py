from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('home.urls', namespace='home')),
    # You can add more URL patterns as needed for other apps or features
]
