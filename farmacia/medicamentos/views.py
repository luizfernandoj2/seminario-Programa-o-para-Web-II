from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Medicamento, Cliente, Venda, Funcionario
from .serializers import MedicamentoSerializer, ClienteSerializer, VendaSerializer

# ViewSet para Medicamentos (API REST)
class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()  # Recupera todos os medicamentos do banco
    serializer_class = MedicamentoSerializer  # Serializador associado
    filter_backends = [DjangoFilterBackend]  # Permite filtragem
    filterset_fields = ['nome', 'validade']  # Filtra por nome e validade

# ViewSet para Clientes (API REST)
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

# ViewSet para Vendas (API REST)
class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

# Página inicial
def home(request):
    return render(request, 'medicamentos/home.html')  # Renderiza o template da home

# Página principal com a lista de medicamentos
def index(request):
    if request.method == "POST":  # Verifica se é uma requisição POST
        nome = request.POST.get('nome')
        lote = request.POST.get('lote')
        validade = request.POST.get('validade')
        preco = request.POST.get('preco')
        quantidade = request.POST.get('quantidade')

        # Cria um novo medicamento
        Medicamento.objects.create(
            nome=nome,
            lote=lote,
            validade=validade,
            preco=preco,
            quantidade=quantidade
        )
        return redirect('index')  # Redireciona para a página principal

    medicamentos = Medicamento.objects.all()  # Recupera todos os medicamentos
    return render(request, 'medicamentos/index.html', {'medicamentos': medicamentos})

# Lista de clientes
def lista_clientes(request):
    clientes = Cliente.objects.all()  # Recupera todos os clientes
    return render(request, 'medicamentos/clientes.html', {'clientes': clientes})

# Lista de vendas
def lista_vendas(request):
    vendas = Venda.objects.select_related('medicamento', 'cliente').all()
    # Usa select_related para otimizar consultas relacionadas
    return render(request, 'medicamentos/vendas.html', {'vendas': vendas})

# Lista de medicamentos
def lista_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    return render(request, 'medicamentos/medicamentos.html', {'medicamentos': medicamentos})

# Lista de funcionários
def lista_funcionarios(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'medicamentos/funcionarios.html', {'funcionarios': funcionarios})

# Página de cadastro (inclui dados para formulários)
def cadastro(request):
    medicamentos = Medicamento.objects.all()
    clientes = Cliente.objects.all()
    return render(request, 'medicamentos/cadastro.html', {
        'medicamentos': medicamentos,
        'clientes': clientes
    })

# Cadastro de medicamento
def cadastrar_medicamento(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        lote = request.POST.get('lote')
        validade = request.POST.get('validade')
        preco = request.POST.get('preco')
        quantidade = request.POST.get('quantidade')

        Medicamento.objects.create(
            nome=nome,
            lote=lote,
            validade=validade,
            preco=preco,
            quantidade=quantidade
        )
        return redirect('cadastro')  # Redireciona para a página de cadastro

# Cadastro de cliente
def cadastrar_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')

        Cliente.objects.create(
            nome=nome,
            cpf=cpf,
            telefone=telefone
        )
        return redirect('cadastro')

# Cadastro de venda
def cadastrar_venda(request):
    if request.method == 'POST':
        medicamento_id = int(request.POST.get('medicamento'))  # ID do medicamento
        cliente_id = int(request.POST.get('cliente'))  # ID do cliente
        quantidade = int(request.POST.get('quantidade'))  # Quantidade vendida

        medicamento = get_object_or_404(Medicamento, id=medicamento_id)
        cliente = get_object_or_404(Cliente, id=cliente_id)

        if medicamento.quantidade < quantidade:
            # Caso estoque insuficiente, exibe mensagem de erro
            return render(request, 'medicamentos/cadastro.html', {
                'error': f'Estoque insuficiente para o medicamento {medicamento.nome}.',
                'medicamentos': Medicamento.objects.all(),
                'clientes': Cliente.objects.all(),
            })

        # Cria a venda e atualiza o estoque
        Venda.objects.create(
            medicamento=medicamento,
            cliente=cliente,
            quantidade=quantidade
        )
        medicamento.quantidade -= quantidade
        medicamento.save()
        return redirect('cadastro')

# Cadastro de funcionário
def cadastrar_funcionario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cargo = request.POST.get('cargo')
        salario = request.POST.get('salario')
        data_contratacao = request.POST.get('data_contratacao')

        Funcionario.objects.create(
            nome=nome,
            cargo=cargo,
            salario=salario,
            data_contratacao=data_contratacao
        )
        return redirect('cadastro')