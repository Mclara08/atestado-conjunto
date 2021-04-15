from django.forms import ModelForm
from app.models import Atestados
from app.models import Empresa

class AtestadosForm(ModelForm):
    class Meta:
        model = Atestados
        fields = ['numero_documento', 'tipo_de_servico', 'data_emissao', 'empresa', 'cliente', 'documento_pdf']
