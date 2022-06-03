from django.contrib import admin
from django.urls import path
from django.urls.conf import include


admin.site.site_header = "TAE Admin"
admin.site.site_title = "TAE Admin Portal"
admin.site.index_title = "Welcome to TEA Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('TAEApp.urls')),
    ]