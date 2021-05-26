import datetime
from io import StringIO

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from app.forms import *
from app.models import Atestados, Cliente, Empresa


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


# home = referente ao index
@login_required(login_url='/entrar')
def home(request):
    if request.user.is_authenticated:
        data = {'db': Atestados.objects.all().order_by('id')}
        return render(request, 'index.html', data)
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('login.html')


# pesquisa = referente à página de pesquisa
def pesquisa(request):
    if request.user.is_authenticated:
        data = {}
        lista_pesquisa = Q(id__gt=0) # Criação da lista de pesquisa

        # Pegando valor atribuido no formulário para número de identificação do documento
        busca_numero = request.GET.get('busca_numero')

        # Pegando valor atribuido no formulário para data de emissão
        busca_data_emissao1 = request.GET.get('busca_data_emissao1')
        busca_data_emissao2 = request.GET.get('busca_data_emissao2')

        # Pegando valor atribuido no formulário para tipo de serviço
        lista_servicos = Q()
        busca_servico_desenv = request.GET.get('busca_servico_desenv')
        busca_servico_its = request.GET.get('busca_servico_its')
        busca_servico_sd = request.GET.get('busca_servico_sd')
        busca_servico_sup = request.GET.get('busca_servico_sup')
        if busca_servico_desenv:
            lista_servicos.add(Q(tipo_de_servico=busca_servico_desenv), Q.OR)
        if busca_servico_its:
            lista_servicos.add(Q(tipo_de_servico=busca_servico_its), Q.OR)
        if busca_servico_sd:
            lista_servicos.add(Q(tipo_de_servico=busca_servico_sd), Q.OR)
        if busca_servico_sup:
            lista_servicos.add(Q(tipo_de_servico=busca_servico_sup), Q.OR)

        # Pegando valor atribuido no formulário para cliente
        lista_cliente = Q()
        i = 0
        while i <= Cliente.objects.all().count():
            if request.GET.get('busca_cliente_' + str(i)):
                busca_cliente = request.GET.get('busca_cliente_' + str(i))
                lista_cliente.add(Q(cliente__id=busca_cliente), Q.OR)
            i += 1

        # Pegando valor atribuido no formulário para empresa
        lista_empresa = Q()
        j = 0
        while j <= Empresa.objects.all().count():
            if request.GET.get('busca_empresa_' + str(j)):
                busca_empresa = request.GET.get('busca_empresa_' + str(j))
                lista_empresa.add(Q(empresa__id=busca_empresa), Q.OR)
            j += 1

        # Pegando valor atribuido no formulário para busca de palavras
        busca_palavra = request.GET.get('busca_palavra')
        lista_palavra = Q()
        if busca_palavra:
            for registro in Atestados.objects.all():
                x = pesquisaPalavra(('media/'+str(registro.documento_pdf)), busca_palavra)
                if x:
                    lista_palavra.add(Q(documento_pdf=registro.documento_pdf), Q.OR)

        # Adicionando atributos na lista para filtrar
        if busca_numero:
            lista_pesquisa.add(Q(numero_documento=busca_numero), Q.AND)
        if busca_data_emissao1 and busca_data_emissao2:
            lista_pesquisa.add(Q(data_emissao__range=[busca_data_emissao1, busca_data_emissao2]), Q.AND)
        elif busca_data_emissao1 or busca_data_emissao2:
            if busca_data_emissao1:
                lista_pesquisa.add(Q(data_emissao=busca_data_emissao1), Q.AND)
            else:
                lista_pesquisa.add(Q(data_emissao=busca_data_emissao2), Q.AND)
        if lista_servicos:
            lista_pesquisa.add(lista_servicos, Q.AND)
        if lista_cliente:
            lista_pesquisa.add(lista_cliente, Q.AND)
        if lista_empresa:
            lista_pesquisa.add(lista_empresa, Q.AND)
        if lista_palavra:
            messages.success(request, "Alguns dos PDFs podem ser ilegíveis, portanto, não aparecerão na tabela abaixo.")
            lista_pesquisa.add(lista_palavra, Q.AND)

        # Verifica existência da lista, filtra de acordo com seu conteúdo e retorna os resultados em páginas
        if lista_pesquisa:
            lista = Atestados.objects.filter(lista_pesquisa).order_by('data_emissao')
            data['clientes'] = Cliente.objects.all()
            data['empresas'] = Empresa.objects.all()
            if lista:
                paginator = Paginator(lista, 6)
                num_pag = request.GET.get('page')
                data['paginas'] = paginator.get_page(num_pag)
                return render(request, 'pesquisa.html', data)
            else:
                messages.error(request, 'Sistema não contém nenhum cadastro com essa(s) especificação(s)!')
                return redirect('pesquisa')
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')

def pesquisaPalavra(caminho, palavras):
    try:
        texto = conversorPdf(caminho)
        if texto.find(palavras.upper()) != -1:
            return caminho
    except:
        return None

def conversorPdf(caminho):
    resource_manager = PDFResourceManager(caching=False)
    out_text = StringIO()
    laParams = LAParams()
    text_converter = TextConverter(resource_manager, out_text, laparams=laParams)
    fp = open(caminho, 'rb')

    interpreter = PDFPageInterpreter(resource_manager, text_converter)

    for page in PDFPage.get_pages(fp, pagenos=set(), password="", caching=False, check_extractable=True):
        interpreter.process_page(page)

    text = out_text.getvalue()
    text = text.replace("\n", " ")

    fp.close()
    text_converter.close()
    out_text.close()
    return text.upper()

def form(request):
    if request.user.is_authenticated:
        data = {'form': AtestadosForm()}
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
                messages.error(request,
                               'Operação não pôde ser realizada! A data de emissão deve ser igual ou inferior à data do dia de hoje.')
                return redirect('form')
            else:
                Atestados.objects.create(numero_documento=form.cleaned_data['numero_documento'],
                                         tipo_de_servico=form.cleaned_data['tipo_de_servico'],
                                         data_emissao=form.cleaned_data['data_emissao'],
                                         empresa=form.cleaned_data['empresa'],
                                         cliente=form.cleaned_data['cliente'],
                                         documento_pdf=form.cleaned_data['documento_pdf'],
                                         created_by=request.user)
                messages.success(request, 'Operação realizada com sucesso!')
                return redirect('form')
        else:
            messages.error(request,
                           'Operação não pôde ser realizada! Por favor, verifique se o número do documento informado já existe na base de dados.')
            return redirect('form')
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')


# Função para visualizar detalhes de atestados cadastrados
def view(request, pk):
    if request.user.is_authenticated:
        data = {'db': Atestados.objects.get(pk=pk)}
        return render(request, 'view.html', data)
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')


# searchall = pesquisa todos os campos
def searchall(request):
    if request.user.is_authenticated:
        data = {}
        todos = Atestados.objects.all().order_by('data_emissao')
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
            data = {'db': Atestados.objects.get(pk=pk)}
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
            data = {'db': Atestados.objects.get(pk=pk)}
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
            messages.error(request,
                           'O atestado selecionado não pertence ao usuário atual, portanto, este não está autenticado para realizar a ação!')
            return redirect('pesquisa')
    else:
        messages.error(request, 'Usuário não conectado!')
        return redirect('entrar')
