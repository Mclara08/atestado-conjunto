from django.contrib import admin
from .models import Atestados

# Register your models here.
@admin.register(Atestados)
class AtestadosAdmin(admin.ModelAdmin):
    list_display = ['id', 'numero_documento']