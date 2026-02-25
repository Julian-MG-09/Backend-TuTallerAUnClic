from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate

from .models import Usuario
from .serializers import UsuarioSerializer


# =====================================
# 🔐 REGISTRO
# =====================================

class RegistroAPIView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]


# =====================================
# 🔑 LOGIN PERSONALIZADO (JWT)
# =====================================

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise ValidationError("Debes enviar username y password.")

        user = authenticate(username=username, password=password)

        if not user:
            raise ValidationError("Credenciales inválidas.")

        if not user.is_active:
            raise ValidationError("Usuario inactivo.")

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "usuario": UsuarioSerializer(user).data
        })


# =====================================
# 🔄 REFRESH TOKEN
# =====================================

class RefreshTokenAPIView(TokenRefreshView):
    permission_classes = [AllowAny]


# =====================================
# 👤 PERFIL DEL USUARIO
# =====================================

class PerfilAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)


# =====================================
# 🔐 CAMBIAR CONTRASEÑA
# =====================================

class CambiarPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):

        password_actual = request.data.get("password_actual")
        password_nueva = request.data.get("password_nueva")

        if not password_actual or not password_nueva:
            raise ValidationError("Debes enviar ambas contraseñas.")

        if not request.user.check_password(password_actual):
            raise ValidationError("La contraseña actual es incorrecta.")

        if len(password_nueva) < 6:
            raise ValidationError("La nueva contraseña debe tener al menos 6 caracteres.")

        request.user.set_password(password_nueva)
        request.user.save()

        return Response({"mensaje": "Contraseña actualizada correctamente"})


# =====================================
# 🚪 LOGOUT (BLACKLIST JWT)
# =====================================

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                raise ValidationError("Debes enviar el refresh token.")

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"mensaje": "Sesión cerrada correctamente"})

        except Exception:
            return Response(
                {"error": "Token inválido o expirado"},
                status=status.HTTP_400_BAD_REQUEST
            )