from django.contrib import admin
from .models import (
    Rol,
    Usuario,
    TipoEstablecimiento,
    Establecimiento,
    TipoServicio,
    Servicio,
    Vehiculo,
    Agenda,
    PrestacionServicio,
    Calificacion,
    Notificacion
)

# ============================
# USUARIOS
# ============================

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre',)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'telefono', 'rol')
    list_filter = ('rol',)
    search_fields = ('username', 'email')


# ============================
# ESTABLECIMIENTOS
# ============================

@admin.register(TipoEstablecimiento)
class TipoEstablecimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


@admin.register(Establecimiento)
class EstablecimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'telefono', 'propietario')
    list_filter = ('tipo',)
    search_fields = ('nombre', 'direccion')


# ============================
# SERVICIOS
# ============================

@admin.register(TipoServicio)
class TipoServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'establecimiento', 'tipo_servicio')
    list_filter = ('tipo_servicio',)


# ============================
# VEHÍCULOS
# ============================

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'usuario')


# ============================
# CITAS
# ============================

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora')


@admin.register(PrestacionServicio)
class PrestacionServicioAdmin(admin.ModelAdmin):
    list_display = ('establecimiento', 'usuario', 'fecha', 'estado')
    list_filter = ('estado',)


# ============================
# CALIFICACIONES
# ============================

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('prestacion', 'puntuacion', 'fecha')


# ============================
# NOTIFICACIONES
# ============================

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'titulo', 'leida', 'fecha')
    list_filter = ('leida',)