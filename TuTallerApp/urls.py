from django.urls import path
from .views import (
    RegistroView,
    LoginView,
    PerfilView,
    VehiculoCreateView,
    MisVehiculosView,
    EstablecimientoListView,
    EstablecimientoDetailView,
    EstablecimientoCreateView,
    ServiciosPorEstablecimientoView,
    ServicioCreateView,
    CrearCitaView,
    MisCitasView,
    CitasEmpresaView,
    CambiarEstadoCitaView,
    DashboardEmpresaView,
    CrearCalificacionView,
    CalificacionesEstablecimientoView,
    MisNotificacionesView,
    MarcarLeidaView,home,login_web
)

urlpatterns = [
    path('', home),
        path('login/', login_web, name='login_web'),
    path('usuarios/register/', RegistroView.as_view()),
    path('usuarios/login/', LoginView.as_view()),
    path('usuarios/perfil/', PerfilView.as_view()),
    path('usuarios/vehiculos/', MisVehiculosView.as_view()),
    path('usuarios/vehiculos/crear/', VehiculoCreateView.as_view()),

    path('establecimientos/', EstablecimientoListView.as_view()),
    path('establecimientos/<int:pk>/', EstablecimientoDetailView.as_view()),
    path('establecimientos/crear/', EstablecimientoCreateView.as_view()),

    path('servicios/establecimiento/<int:establecimiento_id>/', ServiciosPorEstablecimientoView.as_view()),
    path('servicios/crear/', ServicioCreateView.as_view()),

    path('citas/crear/', CrearCitaView.as_view()),
    path('citas/mis-citas/', MisCitasView.as_view()),
    path('citas/empresa/<int:establecimiento_id>/', CitasEmpresaView.as_view()),
    path('citas/<int:pk>/estado/', CambiarEstadoCitaView.as_view()),
    path('citas/dashboard/<int:establecimiento_id>/', DashboardEmpresaView.as_view()),

    path('calificaciones/crear/', CrearCalificacionView.as_view()),
    path('calificaciones/establecimiento/<int:establecimiento_id>/', CalificacionesEstablecimientoView.as_view()),

    path('notificaciones/', MisNotificacionesView.as_view()),
    path('notificaciones/<int:pk>/leida/', MarcarLeidaView.as_view()),
]