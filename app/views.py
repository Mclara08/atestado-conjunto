import datetime as dt

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app.forms import *
from app.models import Atestados
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.core.files.storage import FileSystemStorage

# Create your views here.
def entrar(request):
    return render(request, 'login.html')

@csrf_protect
def submit(request):
    if request.POST:
        usuario = request.POST.get('cpf')
        senha = request.POST.get('senha')
        user = authenticate(username=usuario, password=senha)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            messages.error(request, 'Usuário e senha não coincidem')
            return redirect('entrar')

def sair(request):
    logout(request)
    return redirect('/entrar')

#home = referente ao index
@login_required(login_url='/entrar/')
def home(request):
    if request.user.is_authenticated:
        data = {}
        data['db'] = Atestados.objects.all()
        return render(request, 'index.html', data)
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')

#pesquisa = referente à página de pesquisa
def pesquisa(request):
    if request.user.is_authenticated:
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
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')

def form(request):
    if request.user.is_authenticated:
        data = {}
        data['form'] = AtestadosForm()
        return render(request, 'atestado_form.html', data)
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')

# Função para cadastrar atestados
def create(request):
    if request.user.is_authenticated:
        form = AtestadosForm(request.POST, request.FILES or None)
        if form.is_valid():
            messages.success(request, 'Operação realizada com sucesso!')
            form.save()
            return redirect('form')
        else:
            messages.error(request, 'Operação não pôde ser realizada! Por favor, verifique se o número do documento informado já existe na base de dados.')
            return redirect('form')
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')

# Função para visualizar detalhes de atestados cadastrados
def view(request, pk):
    if request.user.is_authenticated:
        data = {}
        data['db'] = Atestados.objects.get(pk=pk)
        return render(request, 'view.html', data)
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')

#searchall = pesquisa todos os campos
def searchall(request):
    if request.user.is_authenticated:
        dados = {}
        dados['db'] = Atestados.objects.filter(user=request.user)
        return render(request, 'pesquisa.html', dados)
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')

# Função para tela de edição de atestados
def edit(request, pk):
    if request.user.is_authenticated:
        dado = Atestados.objects.get(pk=pk)
        if dado.user == request.user:
            data = {}
            data['db'] = Atestados.objects.get(pk=pk)
            data['form'] = AtestadosForm(instance=data['db'])
            return render(request, 'atestado_form.html', data)
        else:
            messages.error(request, 'O atestado selecionado não pertence ao usuário atual, portanto, este não está autenticado para realizar a ação!')
            return redirect('pesquisa')
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')

# Função para atualizar edições de atestados
def update(request, pk):
    if request.user.is_authenticated:
        data = {}
        data['db'] = Atestados.objects.get(pk=pk)
        form = AtestadosForm(request.POST, request.FILES or None, instance=data['db'])
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')

# Função para deletar atestados
def delete(request, pk):
    if request.user.is_authenticated:
        db = Atestados.objects.get(pk=pk)
        db.delete()
        return redirect('pesquisa')
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')
