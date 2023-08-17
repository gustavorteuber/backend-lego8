from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from .models import Local, Usuario, Registro
from .serializers import LocalSerializer, UsuarioSerializer, RegistroSerializer
from rest_framework import viewsets
from django.db.models import Q
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

class LocalViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer  

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class RegistroViewSet(viewsets.ModelViewSet):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer

class UsuarioProdutividadeView(APIView):
    def get(self, request, id):
        try:
            usuario = Usuario.objects.get(id=id)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        usuario_data = UsuarioSerializer(usuario).data
        usuario_data['produtividade_diaria'] = usuario.calcular_produtividade_diaria()
        usuario_data['produtividade_mensal'] = usuario.calcular_produtividade_mensal()
        usuario_data['produtividade_anual'] = usuario.calcular_produtividade_anual()

        return Response(usuario_data)

def produtividade_operadores(request):
    operadores = Usuario.objects.all()
    data = []

    for operador in operadores:
        data.append({
            'username': operador.user.username,
            'horas_mensais': operador.horas_mensais,
            'produtividade': operador.produtividade,
        })

    return JsonResponse(data, safe=False)


def sum_all_working_hours(request):
    all_operators = Usuario.objects.all()
    total_working_hours = 0
    
    for operator in all_operators:
        total_working_hours += operator.total_horas_trabalhadas()
    
    return JsonResponse({'total_working_hours': total_working_hours})
