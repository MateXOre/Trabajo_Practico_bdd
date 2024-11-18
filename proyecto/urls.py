from django.contrib import admin
from django.urls import path, include 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('aplicacion.urls')),
    path('', include('aplicacion.urls')), 
]

#python manage.py runserver

