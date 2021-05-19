import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app.forms import *
from app.models import Atestados, Cliente, Empresa
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator

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
            return redirect('home')
        else:
            messages.error(request, 'Usuário e senha não coincidem')
            return redirect('entrar')

def sair(request):
    logout(request)
    return redirect('/entrar')

#home = referente ao index
@login_required(login_url='/entrar')
def home(request):
    if request.user.is_authenticated:
        data = {}
        data['db'] = Atestados.objects.all()
        return render(request, 'index.html', data)
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('login.html')

#pesquisa = referente à página de pesquisa
def pesquisa(request):
    if request.user.is_authenticated:
        data = {}

        # Número de identificação do documento
        busca_numero = request.GET.get('busca_numero')

        # Data de emissão
        busca_data_emissao1 = request.GET.get('busca_data_emissao1')
        busca_data_emissao2 = request.GET.get('busca_data_emissao2')

        # Tipo de serviço
        lista_servicos = []
        busca_servico_desenv = request.GET.get('busca_servico_desenv')
        busca_servico_its = request.GET.get('busca_servico_its')
        busca_servico_sd = request.GET.get('busca_servico_sd')
        busca_servico_sup = request.GET.get('busca_servico_sup')
        if busca_servico_desenv:
            lista_servicos.append(busca_servico_desenv)
        if busca_servico_its:
            lista_servicos.append(busca_servico_its)
        if busca_servico_sd:
            lista_servicos.append(busca_servico_sd)
        if busca_servico_sup:
            lista_servicos.append(busca_servico_sup)

        # Cliente
        busca_cliente1 = request.GET.get('busca_cliente_1')
        busca_cliente2 = request.GET.get('busca_cliente_2')
        busca_cliente3 = request.GET.get('busca_cliente_3')
        busca_cliente4 = request.GET.get('busca_cliente_4')

        # Empresa
        busca_empresa1 = request.GET.get('busca_empresa_1')
        busca_empresa2 = request.GET.get('busca_empresa_2')
        busca_empresa3 = request.GET.get('busca_empresa_3')

        lista_pesquisa = Q(id__gt=0)

        if busca_numero:
            lista_pesquisa.add(Q(numero_documento=busca_numero), Q.AND)
        if busca_data_emissao1 and busca_data_emissao2:
            lista_pesquisa.add(Q(data_emissao__range=[busca_data_emissao1, busca_data_emissao2]), Q.AND)
        elif busca_data_emissao1 or busca_data_emissao2:
            if busca_data_emissao1:
                lista_pesquisa.add(Q(data_emissao=busca_data_emissao1), Q.AND)
            else:
                lista_pesquisa.add(Q(data_emissao=busca_data_emissao2), Q.AND)

        for item in lista_servicos:
            i = lista_servicos.__len__() - 1
            if item != lista_servicos[i]:
                lista_pesquisa.add(Q(tipo_de_servico=item), Q.OR)
            else:
                lista_pesquisa.add(Q(tipo_de_servico=item), Q.AND)

        if busca_cliente1:
            lista_pesquisa.add(Q(cliente__id=busca_cliente1), Q.AND)
        if busca_cliente2:
            lista_pesquisa.add(Q(cliente__id=busca_cliente2), Q.AND)
        if busca_cliente3:
            lista_pesquisa.add(Q(cliente__id=busca_cliente3), Q.AND)
        if busca_cliente4:
            lista_pesquisa.add(Q(cliente__id=busca_cliente4), Q.AND)

        if busca_empresa1:
            lista_pesquisa.add(Q(empresa__id=busca_empresa1), Q.AND)
        if busca_empresa2:
            lista_pesquisa.add(Q(empresa__id=busca_empresa2), Q.AND)
        if busca_empresa3:
            lista_pesquisa.add(Q(empresa__id=busca_empresa3), Q.AND)

        if lista_pesquisa != []:
            lista = Atestados.objects.filter(lista_pesquisa)
            data['clientes'] = Cliente.objects.all();
            data['empresas'] = Empresa.objects.all();
            if lista:
                paginator = Paginator(lista, 6)
                num_pag = request.GET.get('page')
                data['paginas'] = paginator.get_page(num_pag)
                return render(request, 'pesquisa.html', data)
            else:
                messages.error(request, 'Sistema não contém nenhum registro com essas especificações!')
                return redirect('pesquisa')
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
            if form.cleaned_data['data_emissao'] > datetime.date.today():
                messages.error(request, 'Operação não pôde ser realizada! A data de emissão deve ser igual ou inferior à data do dia de hoje.')
                return redirect('form')
            else:
                Atestados.objects.create(numero_documento=form.cleaned_data['numero_documento'], tipo_de_servico=form.cleaned_data['tipo_de_servico'],
                                         data_emissao=form.cleaned_data['data_emissao'], empresa=form.cleaned_data['empresa'],
                                         cliente=form.cleaned_data['cliente'], documento_pdf=form.cleaned_data['documento_pdf'],
                                         created_by=request.user)
                messages.success(request, 'Operação realizada com sucesso!')
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
        data = {}
        todos = Atestados.objects.all()
        paginator = Paginator(todos, 6)
        pages = request.GET.get('page')
        data['paginas'] = paginator.get_page(pages)
        return render(request, 'pesquisa.html', data)
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')

# Função para tela de edição de atestados
def edit(request, pk):
    if request.user.is_authenticated:
        dado = Atestados.objects.get(pk=pk)
        if dado.created_by == request.user:
            data = {}
            data['db'] = Atestados.objects.get(pk=pk)
            data['form'] = AtestadosForm(instance=data['db'])
            return render(request, 'atestado_form.html', data)

    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')

# Função para atualizar edições de atestados
def update(request, pk):
    if request.user.is_authenticated:
        dado = Atestados.objects.get(pk=pk)
        if dado.created_by == request.user:
            data = {}
            data['db'] = Atestados.objects.get(pk=pk)
            form = AtestadosForm(request.POST, request.FILES or None, instance=data['db'])
            if form.is_valid():
                Atestados.objects.filter(pk=pk).update(tipo_de_servico=form.cleaned_data['tipo_de_servico'],
                                                       empresa=form.cleaned_data['empresa'],
                                                       cliente=form.cleaned_data['cliente'],
                                                       documento_pdf=form.cleaned_data['documento_pdf'],
                                                       updated_by=request.user)
                return redirect('pesquisa')
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')

# Função para deletar atestados
def delete(request, pk):
    if request.user.is_authenticated:
        dado = Atestados.objects.get(pk=pk)
        if dado.created_by == request.user:
            db = Atestados.objects.get(pk=pk)
            db.delete()
            return redirect('pesquisa')
        else:
            messages.error(request, 'O atestado selecionado não pertence ao usuário atual, portanto, este não está autenticado para realizar a ação!')
            return redirect('pesquisa')
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')
