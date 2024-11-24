from rest_framework import serializers
from .models import Medicamento, Cliente, Venda

# Serializer para o modelo Medicamento
class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento  # Especifica o modelo associado ao serializer
        fields = '__all__'   # Inclui todos os campos do modelo no serializer

# Serializer para o modelo Cliente
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente  # Especifica o modelo associado ao serializer
        fields = '__all__'   # Inclui todos os campos do modelo no serializer

# Serializer para o modelo Venda
class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda  # Especifica o modelo associado ao serializer
        fields = '__all__'   # Inclui todos os campos do modelo no serializer