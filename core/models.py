from django.db import models
from django.contrib.auth.models import User

class Registro(models.Model):
    titulo = models.CharField(max_length=100)
    local = models.CharField(max_length=100)
    data = models.CharField(max_length=100)
    fornecedor = models.CharField(max_length=100)
    peca = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    defeito = models.CharField(max_length=100)
    quantidade_total = models.IntegerField()
    aprovados = models.IntegerField()
    rejeitados = models.IntegerField()
    retrabalhados = models.IntegerField()
    operadores = models.ManyToManyField(User)

    def __str__(self):
        return self.titulo


class RegistroOperador(models.Model):
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE)
    operador = models.ForeignKey(User, on_delete=models.CASCADE)
    hora_inicio = models.CharField(max_length=100, null=True)
    hora_fim = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.registro.titulo} - {self.operador.username}"

