import datetime as dt
from django.shortcuts import render, redirect
from app.forms import *
from app.models import Atestados
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

# Create your views here.
def login(request):
    return render(request, 'login.html')

def home(request):
    data = {}
    data['db'] = Atestados.objects.all()
    return render(request, 'index.html', data)

#pesquisa = referente à página de pesquisa
def pesquisa(request):
    data = {}
    busca_numero = request.GET.get('busca_numero')
    busca_servico = request.GET.get('busca_servico')
    busca_cliente = request.GET.get('busca_cliente')
    busca_data_emissao1 = request.GET.get('busca_data_emissao1')
    busca_data_emissao2 = request.GET.get('busca_data_emissao2')
    busca_empresa = request.GET.get('busca_empresa')
    lista_pesquisa = (Q(id__gt=0))

    if busca_numero:
        lista_pesquisa.add(Q(numero_documento=busca_numero), Q.AND)
    if busca_servico:
        lista_pesquisa.add(Q(tipo_de_servico=busca_servico), Q.AND)
    if busca_cliente:
        lista_pesquisa.add(Q(cliente=busca_cliente), Q.AND)
    if busca_data_emissao1 and busca_data_emissao2:
        lista_pesquisa.add(Q(data_emissao__range=[busca_data_emissao1, busca_data_emissao2]), Q.AND)
    elif busca_data_emissao1 or busca_data_emissao2:
        if busca_data_emissao1:
            lista_pesquisa.add(Q(data_emissao=busca_data_emissao1), Q.AND)
        else:
            lista_pesquisa.add(Q(data_emissao=busca_data_emissao2), Q.AND)
    if busca_empresa:
        lista_pesquisa.add(Q(empresa=busca_empresa), Q.AND)

    if lista_pesquisa == []:
        data['db'] = Atestados.objects.all()
        return render(request, 'pesquisa.html', data)
    else:
        data['db'] = Atestados.objects.filter(lista_pesquisa)
        return render(request, 'pesquisa.html', data)

def form(request):
    data = {}
    data['form'] = AtestadosForm()
    return render(request, 'atestado_form.html', data)

# Função para cadastrar atestados
def create(request):
    form = AtestadosForm(request.POST, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('home')

# Função para visualizar detalhes de atestados cadastrados
def view(request, pk):
    data = {}
    data['db'] = Atestados.objects.get(pk=pk)
    return render(request, 'view.html', data)

#searchall = pesquisa todos os campos
def searchall(request):
    dados = {}
    dados['db'] = Atestados.objects.all()
    return render(request, 'pesquisa.html', dados)

# Função para tela de edição de atestados
def edit(request, pk):
    data = {}
    data['db'] = Atestados.objects.get(pk=pk)
    data['form'] = AtestadosForm(instance=data['db'])
    return render(request, 'atestado_form.html', data)

# Função para atualizar edições de atestados
def update(request, pk):
    data = {}
    data['db'] = Atestados.objects.get(pk=pk)
    form = AtestadosForm(request.POST, request.FILES or None, instance=data['db'])
    if form.is_valid():
        form.save()
        return redirect('home')

# Função para deletar atestados
def delete(request, pk):
    db = Atestados.objects.get(pk=pk)
    db.delete()
    return redirect('pesquisa')
