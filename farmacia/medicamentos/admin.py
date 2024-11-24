from django.contrib import admin
from .models import Medicamento

# Register your models here.

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'lote', 'validade', 'quantidade', 'preco')
    search_fields = ('nome', 'lote')