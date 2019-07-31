from rest_framework import serializers

from .models import Expenses
from .models import Persons
from .models import SheetData


class SheetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SheetData
        fields = ('id', 'display_name', 'description', 'created_date')


class PersonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persons
        fields = ('id', 'name', 'nickname', 'comment', 'created_date', 'sheetId')


class ExpensesSerializer(serializers.ModelSerializer):
    paidTo = serializers.JSONField()

    class Meta:
        model = Expenses
        fields = ('id', 'date', 'description', 'paidBy', 'amount', 'paidTo', 'sheetId')


class PaymentSerializer(serializers.ModelSerializer):
    paidTo = serializers.JSONField()

    class Meta:
        model = Expenses
        fields = ('id','paidBy', 'owes', 'owed', 'owedTo', 'sheetId')
