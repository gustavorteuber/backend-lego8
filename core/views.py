from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from .models import Local, Usuario, Registro, LogsMeses
from .serializers import LocalSerializer, UsuarioSerializer, RegistroSerializer, LogsMesesSerializer
from rest_framework import viewsets
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class LogsMesesList(viewsets.ModelViewSet):
    queryset = LogsMeses.objects.all()
    serializer_class = LogsMesesSerializer

class LocalViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer  

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class RegistroViewSet(viewsets.ModelViewSet):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer

class UsuarioProdutividadeGlobalView(APIView):
    def get(self, request):
        usuarios = Usuario.objects.all()
        data = []

        for usuario in usuarios:
            usuario_data = {
                'username': usuario.user.username,
                'produtividade_dia_anterior': usuario.calcular_produtividade_dia_anterior(),
                'produtividade_diaria': usuario.calcular_produtividade_diaria(),
                'produtividade_mensal': usuario.calcular_produtividade_mensal(),
                'produtividade_anual': usuario.calcular_produtividade_anual(),
            }
            data.append(usuario_data)

        return Response(data)


def sum_all_working_hours(request):
    all_operators = Usuario.objects.all()
    total_working_hours = 0
    
    for operator in all_operators:
        total_working_hours += operator.total_horas_trabalhadas()
    
    return JsonResponse({'total_working_hours': total_working_hours})

