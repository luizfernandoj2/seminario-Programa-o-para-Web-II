from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date, timedelta

# Modelo para Medicamentos
class Medicamento(models.Model):
    nome = models.CharField(max_length=100)  # Nome do medicamento, limite de 100 caracteres
    lote = models.CharField(max_length=50, unique=True)  # Cada lote deve ser único
    validade = models.DateField()  # Data de validade do medicamento
    preco = models.DecimalField(
        max_digits=10, decimal_places=2, 
        validators=[MinValueValidator(0)]
    )  # Preço do medicamento, não pode ser negativo
    quantidade = models.IntegerField(
        validators=[MinValueValidator(0)]
    )  # Quantidade em estoque, não permite valores negativos

    def __str__(self):
        return self.nome  # Representação em string do medicamento (exibido em listagens)

    # Método de classe para identificar medicamentos com estoque abaixo de um limite
    @classmethod
    def estoque_baixo(cls, limite=10):
        return cls.objects.filter(quantidade__lt=limite)  # Medicamentos com estoque abaixo do limite

    # Método de classe para identificar medicamentos com validade próxima
    @classmethod
    def proximos_vencimento(cls, dias=30):
        limite = date.today() + timedelta(days=dias)  # Data limite para próximos vencimentos
        return cls.objects.filter(validade__lte=limite)  # Medicamentos com validade menor ou igual à data limite


# Modelo para Clientes
class Cliente(models.Model):
    nome = models.CharField(max_length=100)  # Nome do cliente, limite de 100 caracteres
    cpf = models.CharField(max_length=11, unique=True)  # CPF único para cada cliente
    telefone = models.CharField(max_length=15, blank=True, null=True)  # Telefone é opcional

    def __str__(self):
        return self.nome  # Representação em string do cliente


# Modelo para Vendas
class Venda(models.Model):
    medicamento = models.ForeignKey(
        Medicamento, on_delete=models.CASCADE
    )  # Relacionamento com Medicamento; exclui vendas se o medicamento for removido
    cliente = models.ForeignKey(
        Cliente, on_delete=models.SET_NULL, null=True, blank=True
    )  # Relacionamento opcional com Cliente
    quantidade = models.IntegerField(
        validators=[MinValueValidator(1)]
    )  # Quantidade vendida, não pode ser menor que 1
    data_venda = models.DateTimeField(auto_now_add=True)  # Data e hora automáticas da venda

    def save(self, *args, **kwargs):
        # Verifica se há estoque suficiente para realizar a venda
        if self.medicamento.quantidade < self.quantidade:
            raise ValidationError(
                f"Estoque insuficiente para o medicamento {self.medicamento.nome}!"
            )
        # Reduz a quantidade do medicamento no estoque
        self.medicamento.quantidade -= self.quantidade
        self.medicamento.save()  # Salva a alteração no estoque
        super().save(*args, **kwargs)  # Salva a venda normalmente

    def __str__(self):
        return f"Venda de {self.medicamento.nome} ({self.quantidade})"  # Representação em string da venda


# Modelo para Funcionários
class Funcionario(models.Model):
    nome = models.CharField(max_length=100)  # Nome do funcionário, limite de 100 caracteres
    cargo = models.CharField(max_length=50)  # Cargo do funcionário
    salario = models.DecimalField(
        max_digits=10, decimal_places=2, 
        validators=[MinValueValidator(0)]
    )  # Salário do funcionário, não pode ser negativo
    data_contratacao = models.DateField()  # Data de contratação do funcionário

    def __str__(self):
        return self.nome  # Representação em string do funcionário