from rest_framework import serializers
from .models import Establecimiento,PrestacionServicio,Servicio,Calificacion,Usuario, Vehiculo






class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'telefono', 'rol', 'password']

    def create(self, validated_data):
        user = Usuario.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            telefono=validated_data['telefono'],
            rol=validated_data.get('rol')
        )
        return user


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'


class EstablecimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establecimiento
        fields = '__all__'



# servicios/serializers.py


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'
#citas/serializers.py

class PrestacionServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrestacionServicio
        fields = '__all__'
        read_only_fields = ['usuario', 'estado']
# calificaciones/serializers.py

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = '__all__'
        
        


from rest_framework import serializers
from .models import Notificacion

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'
        read_only_fields = ['usuario', 'fecha']