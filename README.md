# Cadastro de Atestados
## Repositório em conjunto do projeto de Atestados
<p align="center">Site para cadastro, visualização e download de Atestados</p>
<h4 align="center">Site em construção</h4>

Tabela de conteúdos
===================
<!--ts-->
  * [Sobre](#sobre)
  * [Funcionalidades](#funcionalidades)
  * [Como executar o projeto](#como-executar-o-projeto)
  * [Tecnologias](#tecnologias)
<!--te-->

## Sobre
Sistema para uso interno dos colaboradores, com objetivo de armazenar atestados em uma
base de dados. Com interface web, os usuários do sistema podem encontrar e consultar os
atestados cadastrados na base de dados, utilizando-se de filtros para realizar suas
pesquisas com maior facilidade. Os usuários podem também inserir e excluir atestados do
sistema, além de alterar as informações dos atestados já cadastrados. Para realizar o login
no sistema, os usuários utilizam como credenciais seu CPF, seguido por uma senha
previamente definida. Novos usuários só podem ser cadastrados pelos administradores do
sistema.

## Funcionalidades:
* Usuários:
  * Administradores podem adicionar/excluir usuários;
* Cadastro de Atestados:
  * Administradores podem adicionar/excluir opção de empresa;
  * Administradores podem adicionar/excluir tipos de serviços;
  * Administradores podem adicionar/excluir opção de clientes;
  * Administradores podem adicionar/excluir/alterar/consultar atestados;
  * Usuários podem adicionar/excluir/alterar/consultar atestados;
  
  ## Como executar o projeto
  ### Pré-requisitos
  Antes de começar, usuários do sistema operacional Windows precisarão instalar o controlador
  de versão Git. Sistemas Linux já contam com o Git instalado, mas é possível verificar no
  terminal com o comando git --version.
  #### Executando o projeto:
  ```bash
  # Clone o repositório do projeto
  $ git clone https://github.com/Mclara08/atestado-conjunto.git
  
  # Acesse a pasta do projeto pelo terminal/cmd
  $cd <caminho da pasta>
  
  # Ative a máquina virtual
  $cd <caminho da pasta>/venv/scripts/activate
  
  # Retorne para a pasta do projeto
  $cd <caminho da pasta>/venv/scripts cd ../..
  
  # Instale o framework Django
  $cd <caminho da pasta> python -m pip install Django
  
  # Instale o pacote Django Crispy Forms
  $cd <caminho da pasta> python pip install django-crispy-forms
  
  # Execute o comando runserver
  $cd <caminho da pasta> python manage.py runserver
  
  # Acesse a página através do browser
  http://localhost:8000
  ```
  ---
  ## Tecnologias
  No desenvolvimento deste projeto, foram utilizadas as seguintes tecnologias:
  - **[Python](https://www.python.org/)**
  - **[Django](https://www.djangoproject.com/)**
  - **[Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/)**
  - **[MySQL](https://www.mysql.com/)**
