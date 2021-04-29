from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Atestados)
class AtestadosAdmin(admin.ModelAdmin):
    list_display = ['id', 'numero_documento', 'tipo_de_servico', 'data_emissao', 'empresa', 'cliente', 'documento_pdf', 'created_by', 'updated_by']

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'cnpj']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'cnpj']