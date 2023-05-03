# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Registro, RegistroOperador


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class RegistroSerializer(serializers.ModelSerializer):
    operadores = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True)

    class Meta:
        model = Registro
        fields = '__all__'


class RegistrOpoSerializer(serializers.ModelSerializer):
    operadores = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True)

    class Meta:
        model = RegistroOperador
        fields = '__all__'
