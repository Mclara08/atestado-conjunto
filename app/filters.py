from .models import Atestados
import django_filters

class AtestadosFilter(django_filters.FilterSet):
    class Meta:
        model = Atestados
        fields = ['numero_documento', 'tipo_de_servico', 'data_emissao', 'cliente_id', 'empresa_id']