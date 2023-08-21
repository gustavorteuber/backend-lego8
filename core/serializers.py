from rest_framework import serializers
from core.models import Local, Usuario, Registro, LogsMeses

class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    total_horas_trabalhadas = serializers.ReadOnlyField()
    produtividade = serializers.ReadOnlyField()

    class Meta:
        model = Usuario
        fields = '__all__'

class RegistroSerializer(serializers.ModelSerializer):
    horas_trabalhadas = serializers.ReadOnlyField()

    class Meta:
        model = Registro
        fields = '__all__'

class LogsMesesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogsMeses
        fields = '__all__'