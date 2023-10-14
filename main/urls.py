from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('charts/', include('charts.urls')),  # Include the "charts" app's URLs
]
