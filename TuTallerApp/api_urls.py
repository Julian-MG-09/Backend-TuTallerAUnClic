from django.urls import path

# ==============================
# 🔐 AUTENTICACIÓN
# ==============================

from .auth_api import (
    RegistroAPIView,
    LoginAPIView,
    RefreshTokenAPIView,
    PerfilAPIView,
    CambiarPasswordAPIView,
    LogoutAPIView
)

# ==============================
# 🧠 LÓGICA DEL NEGOCIO
# ==============================

from .api import (
    EstablecimientoListAPIView,
    EstablecimientoDetailAPIView,
    EstablecimientoCreateAPIView,
    ServiciosPorEstablecimientoAPIView,
    ServicioCreateAPIView,
    VehiculoCreateAPIView,
    MisVehiculosAPIView,
    CrearCitaAPIView,
    MisCitasAPIView,
    CitasEmpresaAPIView,
    CambiarEstadoCitaAPIView,
    CrearCalificacionAPIView,
    CalificacionesEstablecimientoAPIView,
    DashboardEmpresaAPIView,
    MisNotificacionesAPIView,
    MarcarLeidaAPIView
)

urlpatterns = [

    # =====================================
    # 🔐 AUTH
    # =====================================
    path('auth/register/', RegistroAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),
    path('auth/refresh/', RefreshTokenAPIView.as_view()),
    path('auth/logout/', LogoutAPIView.as_view()),
    path('auth/perfil/', PerfilAPIView.as_view()),
    path('auth/cambiar-password/', CambiarPasswordAPIView.as_view()),

    # =====================================
    # 🏢 ESTABLECIMIENTOS
    # =====================================
    path('establecimientos/', EstablecimientoListAPIView.as_view()),
    path('establecimientos/<int:pk>/', EstablecimientoDetailAPIView.as_view()),
    path('establecimientos/crear/', EstablecimientoCreateAPIView.as_view()),

    # =====================================
    # 🛠 SERVICIOS
    # =====================================
    path('servicios/establecimiento/<int:establecimiento_id>/', ServiciosPorEstablecimientoAPIView.as_view()),
    path('servicios/crear/', ServicioCreateAPIView.as_view()),

    # =====================================
    # 🚗 VEHÍCULOS
    # =====================================
    path('vehiculos/', MisVehiculosAPIView.as_view()),
    path('vehiculos/crear/', VehiculoCreateAPIView.as_view()),

    # =====================================
    # 📅 CITAS
    # =====================================
    path('citas/crear/', CrearCitaAPIView.as_view()),
    path('citas/mis/', MisCitasAPIView.as_view()),
    path('citas/empresa/', CitasEmpresaAPIView.as_view()),
    path('citas/<int:pk>/estado/', CambiarEstadoCitaAPIView.as_view()),

    # =====================================
    # ⭐ CALIFICACIONES
    # =====================================
    path('calificaciones/crear/', CrearCalificacionAPIView.as_view()),
    path('calificaciones/establecimiento/<int:establecimiento_id>/', CalificacionesEstablecimientoAPIView.as_view()),

    # =====================================
    # 📊 DASHBOARD
    # =====================================
    path('dashboard/empresa/', DashboardEmpresaAPIView.as_view()),

    # =====================================
    # 🔔 NOTIFICACIONES
    # =====================================
    path('notificaciones/', MisNotificacionesAPIView.as_view()),
    path('notificaciones/<int:pk>/leida/', MarcarLeidaAPIView.as_view()),
]