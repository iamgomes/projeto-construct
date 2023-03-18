from django.http import HttpResponse
from django.shortcuts import render
from rolepermissions.decorators import has_permission_decorator
from .models import Users
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.contrib import messages


@has_permission_decorator('cadastrar_vendedor')
def cadastrar_vendedor(request):
    if request.method == 'GET':
        vendedores = Users.objects.filter(cargo='V')
        return render(request, 'cadastrar_vendedor.html', {'vendedores':vendedores})
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = Users.objects.filter(email=email)

        if user.exists():
            return HttpResponse('Email já existe')

        user = Users.objects.create_user(username=email, email=email, password=senha, 
                                        first_name=nome, last_name=sobrenome, cargo='V')

        return HttpResponse('Conta Criada')


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse('plataforma'))
        return render(request, 'login.html')
    elif request.method == 'POST':
        login = request.POST.get('email')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=login, password=senha)

        if not user:
            return HttpResponse('Usuário inválido')

        auth.login(request, user)
        return HttpResponse('Usuário logado com sucesso')


def logout(resquest):
    resquest.session.flush()
    return redirect(reverse('login'))


@has_permission_decorator('cadastrar_vendedor')
def excluir_usuario(request, id):
    vendedor = get_object_or_404(Users, pk=id)
    vendedor.delete()
    messages.add_message(request, messages.SUCCESS, 'Vendedor excluído com sucesso!')
    return redirect(reverse('cadastrar_vendedor'))