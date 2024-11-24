"""
URL configuration for farmacia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from medicamentos.views import home, MedicamentoViewSet, ClienteViewSet, VendaViewSet
from medicamentos.views import index
from medicamentos.views import lista_clientes
from medicamentos.views import lista_vendas
from medicamentos.views import lista_medicamentos
from medicamentos.views import lista_funcionarios
from medicamentos.views import cadastro
from medicamentos.views import cadastrar_cliente, cadastrar_funcionario, cadastrar_medicamento, cadastrar_venda

router = DefaultRouter()
router.register(r'medicamentos', MedicamentoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'vendas', VendaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', home, name='home'),
    path('', index, name='index'),
    path('clientes/', lista_clientes, name='lista_clientes'),
    path('vendas/', lista_vendas, name='lista_vendas'),
    path('medicamentos/', lista_medicamentos, name='lista_medicamentos'),
    path('funcionarios/', lista_funcionarios, name='lista_funcionarios'),
    path('cadastro/', cadastro, name='cadastro'),
    path('cadastrar-funcionario/', cadastrar_funcionario, name='cadastrar_funcionario'),
    path('cadastrar-cliente/', cadastrar_cliente, name='cadastrar_cliente'),
    path('cadastrar-medicamento/', cadastrar_medicamento, name='cadastrar_medicamento'),
    path('cadastrar-venda/', cadastrar_venda, name='cadastrar_venda'),
]
