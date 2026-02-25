from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Incluye TODAS las rutas de TuTallerApp
    path('', include('TuTallerApp.urls')),
]