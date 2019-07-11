from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Expenses
from .models import ComputePayment
from .models import Persons
from .models import SheetData
from .serializers import ExpensesSerializer
from .serializers import PersonsSerializer
from .serializers import SheetDataSerializer



class ComputePayment(APIView):
    def put(self,request):
            pk = request._request.GET['pk']
            expenses = Expenses.objects.filter(sheetId_id=pk).values('amount','paidTo',"paidBy")
            payment=ComputePayment.objects.all()
            for i in expenses:
                print(i['amount'])



