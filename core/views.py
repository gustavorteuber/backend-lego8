# views.py
from rest_framework import viewsets
from django.contrib.auth.models import User
from core.models import Registro, RegistroOperador
from core.serializers import RegistroSerializer, UserSerializer, RegistrOpoSerializer, DetailRegistroSerializer, RegistropDetail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['id'] = self.user.id
        data['email'] = self.user.email
        data['is_superuser'] = self.user.is_superuser

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegistroViewSet(viewsets.ModelViewSet):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return DetailRegistroSerializer
        return RegistroSerializer


class RegistroOpViewSet(viewsets.ModelViewSet):
    queryset = RegistroOperador.objects.all()
    serializer_class = RegistrOpoSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return RegistropDetail
        return RegistrOpoSerializer