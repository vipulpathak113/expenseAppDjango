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
from django.db import connection
from django.core.paginator import Paginator



class ComputePayment(APIView):
    def put(self,request):
            pk = request._request.GET['pk']
            expenses = Expenses.objects.filter(sheetId_id=pk).values('amount','paidTo',"paidBy")
            payment=ComputePayment.objects.all()
            for i in expenses:
                print(i['amount'])
    def get(self, request):
        if request.method == 'GET':
            pk = request._request.GET['pk']
            pageNo = request._request.GET['pageNo']
            expenses = Expenses.objects.filter(sheetId_id=pk).values_list("date", "description", "paidBy__nickname",
                                                                          "amount", "paidTo", "id")
            count = Expenses.objects.filter(sheetId_id=pk).count()

            paginator = Paginator(expenses, 2)
            page = paginator.page(pageNo)
            object= page.object_list
            if expenses:
                return Response({"expenses":object,"count":count})
            else:
                return Response("NO DATA FOUND", status=status.HTTP_204_NO_CONTENT)


