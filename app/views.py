from django.shortcuts import render, redirect
from app.forms import *
from app.models import Atestados
from django.core.files.storage import FileSystemStorage

# Create your views here.
def home(request):
    data = {}
    data['db'] = Atestados.objects.all()
    return render(request, 'index.html', data)

#pesquisa = referente à página de pesquisa
def pesquisa(request):
    data = {}
    data['db'] = Atestados.objects.all()
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

#search = método que pega o conteúdo de um formulário
def search(request):
    data = {}
    if request.method=="POST":
        numero=request.POST.get('numero')
        cliente=request.POST.get('cliente')
        servico=request.POST.get('servico')
        date=request.POST.get('data')
        empresa=request.POST.get('empresa')
        data['atestados'] = Atestados.objects.all().raw('select * from app_atestados where numero_documento = %s and tipo_de_servico = %s', [numero], [servico])
        return render(request, 'pesquisa.html', data)
    else:
        data['dados'] = Atestados.objects.all()
        return render(request, 'pesquisa.html', data)

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
