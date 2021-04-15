from django.db import models
from datetime import datetime

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

class Atestados(models.Model):
    numero_documento = models.CharField(max_length=30)

    servico = (('Desenvolvimento', 'Desenvolvimento'),
               ('ITS', 'ITS'),
               ('Service Desk', 'Service Desk'),
               ('Suporte', 'Suporte'),
               )

    tipo_de_servico = models.CharField(max_length=30, choices=servico, blank=True)
    data_emissao = models.DateField(default=datetime.now)
    empresa = models.ForeignKey(Empresa, on_delete=models.RESTRICT, null=False, related_name='rel_empresa')
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, null=False, related_name='rel_cliente')
    documento_pdf = models.FileField(upload_to='atestados/PDFs/')

    def delete(self, *args, **kwargs):
        self.documento_pdf.delete()
        super().delete(*args, **kwargs)
