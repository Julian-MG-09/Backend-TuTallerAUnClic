from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import (
    Usuario,
    Establecimiento,
    Servicio,
    Vehiculo,
    PrestacionServicio,
    Calificacion,
    Notificacion
)

from .serializers import (
    UsuarioSerializer,
    EstablecimientoSerializer,
    ServicioSerializer,
    VehiculoSerializer,
    PrestacionServicioSerializer,
    CalificacionSerializer,
    NotificacionSerializer
)

from usuarios.permissions import EsCliente, EsEmpresa, EsAdmin


# =====================================
# 🔐 AUTENTICACIÓN
# =====================================

class RegistroAPIView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class LoginAPIView(TokenObtainPairView):
    pass


class PerfilAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)


# =====================================
# 🏢 ESTABLECIMIENTOS
# =====================================

class EstablecimientoListAPIView(generics.ListAPIView):
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer


class EstablecimientoDetailAPIView(generics.RetrieveAPIView):
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer


class EstablecimientoCreateAPIView(generics.CreateAPIView):
    serializer_class = EstablecimientoSerializer
    permission_classes = [EsAdmin]

    def perform_create(self, serializer):
        serializer.save(propietario=self.request.user)


# =====================================
# 🛠 SERVICIOS
# =====================================

class ServiciosPorEstablecimientoAPIView(generics.ListAPIView):
    serializer_class = ServicioSerializer

    def get_queryset(self):
        return Servicio.objects.filter(
            establecimiento_id=self.kwargs['establecimiento_id']
        )


class ServicioCreateAPIView(generics.CreateAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [EsEmpresa]


# =====================================
# 🚗 VEHÍCULOS
# =====================================

class VehiculoCreateAPIView(generics.CreateAPIView):
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class MisVehiculosAPIView(generics.ListAPIView):
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Vehiculo.objects.filter(usuario=self.request.user)


# =====================================
# 📅 CITAS
# =====================================

class CrearCitaAPIView(generics.CreateAPIView):
    serializer_class = PrestacionServicioSerializer
    permission_classes = [EsCliente]

    def perform_create(self, serializer):

        establecimiento = serializer.validated_data['establecimiento']
        agenda = serializer.validated_data['agenda']
        fecha = serializer.validated_data['fecha']

        # Validar horario
        if not (establecimiento.hora_apertura <= agenda.hora <= establecimiento.hora_cierre):
            raise ValidationError("Horario fuera del rango permitido.")

        # Evitar doble reserva
        if PrestacionServicio.objects.filter(
            establecimiento=establecimiento,
            agenda=agenda,
            fecha=fecha,
            estado__in=['pendiente', 'confirmada']
        ).exists():
            raise ValidationError("Ese horario ya está reservado.")

        cita = serializer.save(
            usuario=self.request.user,
            estado='pendiente'
        )

        # 🔔 Notificar empresa
        Notificacion.objects.create(
            usuario=cita.establecimiento.propietario,
            titulo="Nueva cita",
            mensaje=f"Tienes una nueva cita para el {cita.fecha}"
        )


class MisCitasAPIView(generics.ListAPIView):
    serializer_class = PrestacionServicioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PrestacionServicio.objects.filter(usuario=self.request.user)


class CitasEmpresaAPIView(generics.ListAPIView):
    serializer_class = PrestacionServicioSerializer
    permission_classes = [EsEmpresa]

    def get_queryset(self):
        return PrestacionServicio.objects.filter(
            establecimiento__propietario=self.request.user
        )


class CambiarEstadoCitaAPIView(APIView):
    permission_classes = [EsEmpresa]

    def patch(self, request, pk):

        try:
            cita = PrestacionServicio.objects.get(
                pk=pk,
                establecimiento__propietario=request.user
            )
        except PrestacionServicio.DoesNotExist:
            raise ValidationError("No tienes permiso para modificar esta cita.")

        nuevo_estado = request.data.get("estado")

        estados_validos = [
            e[0] for e in PrestacionServicio._meta.get_field('estado').choices
        ]

        if nuevo_estado not in estados_validos:
            raise ValidationError("Estado inválido.")

        cita.estado = nuevo_estado
        cita.save()

        # 🔔 Notificar cliente
        Notificacion.objects.create(
            usuario=cita.usuario,
            titulo="Estado actualizado",
            mensaje=f"Tu cita fue {cita.estado}"
        )

        return Response({"mensaje": "Estado actualizado correctamente"})


# =====================================
# ⭐ CALIFICACIONES
# =====================================

class CrearCalificacionAPIView(generics.CreateAPIView):
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated]


class CalificacionesEstablecimientoAPIView(generics.ListAPIView):
    serializer_class = CalificacionSerializer

    def get_queryset(self):
        return Calificacion.objects.filter(
            prestacion__establecimiento_id=self.kwargs['establecimiento_id']
        )


# =====================================
# 📊 DASHBOARD
# =====================================

class DashboardEmpresaAPIView(APIView):
    permission_classes = [EsEmpresa]

    def get(self, request):

        total = PrestacionServicio.objects.filter(
            establecimiento__propietario=request.user
        ).count()

        pendientes = PrestacionServicio.objects.filter(
            establecimiento__propietario=request.user,
            estado='pendiente'
        ).count()

        return Response({
            "total_citas": total,
            "pendientes": pendientes
        })


# =====================================
# 🔔 NOTIFICACIONES
# =====================================

class MisNotificacionesAPIView(generics.ListAPIView):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notificacion.objects.filter(
            usuario=self.request.user
        ).order_by('-fecha')


class MarcarLeidaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        notificacion = Notificacion.objects.get(
            pk=pk,
            usuario=request.user
        )

        notificacion.leida = True
        notificacion.save()

        return Response({"mensaje": "Notificación marcada como leída"})