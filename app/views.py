from django.http import HttpResponseRedirect, HttpResponse
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
    data['form'] = AtestadosForm()
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
    form = AtestadosForm()
    atestados = list(Atestados.objects.prefetch_related('empresa').prefetch_related('cliente').all())
    lista = []
    if request.method == "POST":
        f = AtestadosForm(request.POST)
        if f.is_valid():
            numero = request.POST.get('numero_documento')
            return HttpResponse('numero_documento')
            servico = request.POST.get('tipo_de_servico')
            return HttpResponse('tipo_de_servico')
            data_emissao = request.POST.get('data_emissao')
            return HttpResponse('data_emissao')
            cliente = request.POST.get('cliente')
            return HttpResponse('cliente')
            empresa = request.POST.get('empresa')
            return HttpResponse('empresa')

            # Atestado = Atestados.objects.filter(numero_documento=f.cleaned_data["numero_documento"])
            # return HttpResponseRedirect("pesquisa.html", {"atestados": Atestado}, {"form": form})
            # for atest in atestados:
            #     if atest.numero_documento == numero:
            #         lista.append(atest)
            #         data['atestados'] = lista
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
