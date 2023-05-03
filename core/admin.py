from django.contrib import admin
from core.models import Registro


class RegistroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'local', 'data', 'fornecedor', 'peca', 'codigo',
                    'defeito', 'quantidade_total', 'aprovados', 'retrabalhados', 'get_operadores')

    def get_operadores(self, obj):
        return ", ".join([str(u) for u in obj.operadores.all()])
    get_operadores.short_description = 'Operadores'


admin.site.register(Registro, RegistroAdmin)
