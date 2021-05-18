from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Empresa(models.Model):
    nome = models.CharField(max_length=30)
    cnpj = models.CharField(max_length=18)
    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=30)
    cnpj = models.CharField(max_length=18)
    def __str__(self):
        return self.nome

NULL_AND_BLANK = {'null':True, 'blank':True}

class BaseModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by', **NULL_AND_BLANK)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by', **NULL_AND_BLANK)

    class Meta:
        abstract = True

class Atestados(BaseModel):
    numero_documento = models.PositiveBigIntegerField(unique=True)

    servico = (('Desenvolvimento', 'Desenvolvimento'),
               ('ITS', 'ITS'),
               ('Service Desk', 'Service Desk'),
               ('Suporte', 'Suporte'),
               )

    tipo_de_servico = models.CharField(max_length=30, choices=servico, blank=True)
    data_emissao = models.DateField(default=datetime.today)
    empresa = models.ForeignKey(Empresa, on_delete=models.RESTRICT, null=False, related_name='rel_empresa')
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, null=False, related_name='rel_cliente')
    documento_pdf = models.FileField(upload_to='atestados/PDFs/')

    def __getnumero__(self):
        self.numero_documento

    def __getservico__(self):
        self.tipo_de_servico

    def delete(self, *args, **kwargs):
        self.documento_pdf.delete()
        super().delete(*args, **kwargs)
