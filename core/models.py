from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

class Local(models.Model):
    nome = models.CharField(max_length=100)

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    horas_mensais = models.PositiveIntegerField(default=80)
    produtividade = models.FloatField(default=0.0)  # Campo para armazenar a produtividade

    def total_horas_trabalhadas(self):
        registros = Registro.objects.filter(
            Q(operador_1=self.user) | Q(operador_2=self.user) |
            Q(operador_3=self.user) | Q(operador_4=self.user)
        )
        total_horas = sum(registro.horas_trabalhadas() for registro in registros)
        return total_horas

    def calcular_produtividade_diaria(self):
        today = timezone.now().date()
        registros = Registro.objects.filter(
            Q(operador_1=self.user) | Q(operador_2=self.user) |
            Q(operador_3=self.user) | Q(operador_4=self.user),
            data=today
        )
        total_horas = sum(registro.horas_trabalhadas() for registro in registros)
        produtividade_diaria = (total_horas / self.horas_mensais) * 100
        return produtividade_diaria

    def calcular_produtividade_mensal(self):
        today = timezone.now().date()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        registros = Registro.objects.filter(
            Q(operador_1=self.user) | Q(operador_2=self.user) |
            Q(operador_3=self.user) | Q(operador_4=self.user),
            data__range=(first_day_of_month, last_day_of_month)
        )
        
        total_horas = sum(registro.horas_trabalhadas() for registro in registros)
        produtividade_mensal = (total_horas / self.horas_mensais) * 100
        return produtividade_mensal

    def calcular_produtividade_anual(self):
        today = timezone.now().date()
        first_day_of_year = today.replace(month=1, day=1)
        last_day_of_year = today.replace(month=12, day=31)
        
        registros = Registro.objects.filter(
            Q(operador_1=self.user) | Q(operador_2=self.user) |
            Q(operador_3=self.user) | Q(operador_4=self.user),
            data__range=(first_day_of_year, last_day_of_year)
        )
        
        total_horas = sum(registro.horas_trabalhadas() for registro in registros)
        produtividade_anual = (total_horas / self.horas_mensais) * 100
        return produtividade_anual
class Registro(models.Model):
    titulo = models.CharField(max_length=100)
    local = models.ForeignKey('Local', on_delete=models.CASCADE)
    data = models.CharField(max_length=100)
    fornecedor = models.CharField(max_length=100)
    peca = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    defeito = models.CharField(max_length=100)
    quantidade_total = models.IntegerField()
    aprovados = models.IntegerField()
    rejeitados = models.IntegerField()
    retrabalhados = models.IntegerField()
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registros_criados')
    data_fabricacao = models.CharField(max_length=100)
    operador_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registros_operador_1')
    horario_inicio_1 = models.TimeField(default='00:00')
    horario_fim_1 = models.TimeField(default='00:00')
    operador_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registros_operador_2', blank=True, null=True)
    horario_inicio_2 = models.TimeField(default='00:00', blank=True, null=True)
    horario_fim_2 = models.TimeField(default='00:00', blank=True, null=True)
    operador_3 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registros_operador_3', blank=True, null=True)
    horario_inicio_3 = models.TimeField(default='00:00', blank=True, null=True)
    horario_fim_3 = models.TimeField(default='00:00', blank=True, null=True)
    operador_4 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registros_operador_4', blank=True, null=True)
    horario_inicio_4 = models.TimeField(default='00:00', blank=True, null=True)
    horario_fim_4 = models.TimeField(default='00:00', blank=True, null=True)

    def horas_trabalhadas(self):
        total_horas = 0
    
        for i in range(1, 5):
            horario_inicio = getattr(self, f'horario_inicio_{i}')
            horario_fim = getattr(self, f'horario_fim_{i}')
            
            if horario_inicio and horario_fim:
                inicio = datetime.combine(datetime.today(), horario_inicio)
                fim = datetime.combine(datetime.today(), horario_fim)
                
                if fim < inicio:
                    fim += timedelta(days=1) 
                
                total_horas += (fim - inicio).total_seconds() / 3600
        
        return total_horas


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        operators = [
            self.operador_1,
            self.operador_2,
            self.operador_3,
            self.operador_4,
        ]
        
        for operator in operators:
            if operator:
                usuario = operator.usuario
                usuario.produtividade = usuario.calcular_produtividade()
                usuario.save()

@receiver(post_save, sender=Registro)
def update_operator_productivity(sender, instance, created, **kwargs):
    if created:
        operators = [
            instance.operador_1,
            instance.operador_2,
            instance.operador_3,
            instance.operador_4,
        ]
        
        for operator in operators:
            if operator:
                usuario = operator.usuario
                usuario.produtividade = usuario.calcular_produtividade()
                usuario.save()
