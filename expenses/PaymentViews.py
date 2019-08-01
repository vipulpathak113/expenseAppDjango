from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Expenses
from .models import Compute
from .models import Persons
from .models import SheetData
from .serializers import ExpensesSerializer
from .serializers import PersonsSerializer
from .serializers import SheetDataSerializer
from .serializers import PaymentSerializer
from django.db import connection
from django.core.paginator import Paginator


class ComputePayment(APIView):

    def post(self, request):
        if request.method == 'POST':
            expenseData = request.data
            expenseData.update({'paidBy_id  ': request.data['paidBy']})
            print("paidTo",expenseData["paidTo"])
            for i in expenseData["paidTo"]:
                pay=Compute(owed=int(expenseData["amount"])/len(expenseData["paidTo"]),sheetId_id=expenseData["sheetId"],owedTo_id=i,paidBy_id=expenseData["paidBy"])
                pay.save(force_insert=True)

    def get(self, request):
        if request.method == 'GET':
            pk = request._request.GET['pk']
            pageNo = request._request.GET['pageNo']
            filter = request._request.GET['filter']
            print(filter)
            if filter == 'all':
                expenses = Expenses.objects.filter(sheetId_id=pk).values_list("date","description","paidBy__nickname","amount","paidTo", "id").order_by('date')
                count = Expenses.objects.filter(sheetId_id=pk).count()
            else:
                expenses = Expenses.objects.filter(sheetId_id=pk,paidBy__nickname=filter).values_list("date", "description", "paidBy__nickname",
                                                                          "amount", "paidTo", "id").order_by('date')
                count = Expenses.objects.filter(sheetId_id=pk,paidBy__nickname=filter).count()

            paginator = Paginator(expenses,10)
            page = paginator.page(pageNo)
            object = page.object_list
            if expenses:
                return Response({"expenses": object, "count": count})
            else:
                return Response("NO DATA FOUND", status=status.HTTP_204_NO_CONTENT)


class ExpenseFilter(APIView):
    def get(self, request):
        if request.method == 'GET':
            pk = request._request.GET['pk']
            pageNo = request._request.GET['pageNo']
            id= request._request.GET['id']
            expenses = Expenses.objects.filter(paidBy__nickname=pk,sheetId_id=id).values_list("date", "description", "paidBy__nickname",
                                                                         "amount", "paidTo", "id").order_by('date')
            count = Expenses.objects.filter(paidBy__nickname=pk,sheetId_id=id).count()
            paginator = Paginator(expenses, 10)
            page = paginator.page(pageNo)
            object = page.object_list

            if expenses:
                return Response({"expenses":object,"count": count})
            else:
                return Response("NO DATA FOUND", status=status.HTTP_204_NO_CONTENT)


class FilterExpense(APIView):
    def get(self, request):
        if request.method == 'GET':
            pk = request._request.GET['pk']
            items = request._request.GET['items']
            filter= request._request.GET['filter']
            if filter=='all':
                expenses = Expenses.objects.filter(sheetId_id=pk).values_list("date","description","paidBy__nickname","amount","paidTo", "id").order_by('date')
                count = Expenses.objects.filter(sheetId_id=pk).count()
            else:
                expenses = Expenses.objects.filter(sheetId_id=pk,paidBy__nickname=filter).values_list("date", "description", "paidBy__nickname",
                                                                          "amount", "paidTo", "id").order_by('date')
                count = Expenses.objects.filter(sheetId_id=pk, paidBy__nickname=filter).count()
            paginator = Paginator(expenses, items)
            page = paginator.page(1)
            object = page.object_list
            if expenses:
                return Response({"expenses": object,"count": count})
            else:
                return Response("NO DATA FOUND", status=status.HTTP_204_NO_CONTENT)

