from django.forms import ModelForm
from app.models import Atestados
from django import forms

class AtestadosForm(ModelForm):
    class Meta:
        model = Atestados
        fields = ['numero_documento', 'tipo_de_servico', 'data_emissao', 'empresa', 'cliente', 'documento_pdf']

