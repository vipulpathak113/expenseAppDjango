from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Expenses
from .models import Persons
from .models import SheetData
from .models import Compute
from .serializers import ExpensesSerializer
from .serializers import PersonsSerializer
from .serializers import SheetDataSerializer
from .serializers import PaymentSerializer
from django.core.paginator import Paginator, EmptyPage


class SheetDetail(APIView):

    def get(self, request):
        if request.method == 'GET':
            pk = request._request.GET['pk']
            sheets = SheetData.objects.filter(pk=pk)
            serializer = SheetDataSerializer(sheets, many=True)
            return Response(serializer.data)

    def post(self, request):
        if request.method == 'POST':
            serializer = SheetDataSerializer(data=request.data)
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        pk = request._request.GET['pk']
        print(self)
        sheets = SheetData.objects.filter(pk=pk).last()
        serializer = SheetDataSerializer(sheets, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = request._request.GET['pk']
        sheets = SheetData.objects.filter(pk=pk).last()
        sheets.delete()
        return Response("SUCCESSFULLY DELETED", status=status.HTTP_204_NO_CONTENT)


class PersonDetail(APIView):
    def get(self, request):
        if request.method == 'GET':
            pk = request._request.GET['pk']
            persons = Persons.objects.filter(sheetId_id=pk)
            if persons:
                serializer = PersonsSerializer(persons, many=True)
                return Response(serializer.data)
            else:
                return Response("NO DATA FOUND", status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        if request.method == 'POST':
            sheetObj = SheetData.objects.filter(sheet=request.data['sheetId']).last()
            print(sheetObj)
            personData = request.data
            personData.update({'sheetId_id ': sheetObj})
            print("helooooo", personData)
            serializer = PersonsSerializer(data=personData)
            print("serializer", serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        pk = request._request.GET['pk']
        data = request.data
        sheets = Persons.objects.filter(pk=pk).last()
        sheets.name = data.get('name')
        sheets.nickname = data.get('nickname')
        sheets.comment = data.get('comment')
        sheets.save()
        serializer = PersonsSerializer(sheets, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = request._request.GET['pk']
        sheets = Persons.objects.filter(pk=pk).last()
        if sheets:
            sheets.delete()
            return Response("SUCCESSFULLY DELETED", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("DATA DOES NOT EXIST", status=status.HTTP_404_NOT_FOUND)


class ExpenseDetail(APIView):
    def get(self, request):
        if request.method == 'GET':
            pk = request._request.GET['pk']
            pageNo = request._request.GET['pageNo']
            expenses = Expenses.objects.filter(sheetId_id=pk).values_list("date", "description", "paidBy__nickname",
                                                                          "amount", "paidTo", "id").order_by('date')
            print("pageNo",pageNo)
            count = Expenses.objects.filter(sheetId_id=pk).count()
            paginator = Paginator(expenses, 10)
            print("paginator",paginator)
            try:
                page = paginator.page(pageNo)
                object = page.object_list
            except EmptyPage:
                page = paginator.page(int(pageNo)-1)
                object = page.object_list

            if object:
                # serializer = ExpensesSerializer(expenses, many=True)

                return Response({"expenses":object,"count":count})
            else:
                return Response("NO DATA FOUND", status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        if request.method == 'POST':
            # personObj = Persons.objects.filter(nickname=request.data['paidBy']).last()
            # print(personObj)
            expenseData = request.data
            expenseData.update({'paidBy_id  ': request.data['paidBy']})
            print("helooooo", expenseData)
            serializer = ExpensesSerializer(data=expenseData)
            print("serializer", serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if request.method == 'PUT':
            pk = request._request.GET['pk']
            eid = request._request.GET['eid']
            data = request.data
            expenses = Expenses.objects.filter(sheetId_id=pk, id=eid).last()
            # import pdb;
            # pdb.set_trace()
            expenses.date = data.get('date')
            expenses.description = data.get('description')
            expenses.paidBy_id = data.get('paidBy')
            expenses.amount = data.get('amount')
            expenses.paidTo = data.get('paidTo')
            expenses.sheetId_id = data.get('sheetId')
            expenses.save()
            serializer = ExpensesSerializer(expenses, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = request._request.GET['pk']
        expenses = Expenses.objects.filter(pk=pk).last()
        if expenses:
            expenses.delete()
            return Response("SUCCESSFULLY DELETED", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("DATA DOES NOT EXIST", status=status.HTTP_404_NOT_FOUND)


class CountDetail(APIView):
    def get(self, request):
        if request.method == 'GET':
            pk = request._request.GET['pk']
            sheets = Expenses.objects.filter(sheetId_id=pk).aggregate(Sum('amount'))
            return Response(sheets)


class PaymentDetail(APIView):
    def get(self,request):
        if request.method == 'GET':
            pk = request._request.GET['pk']
            # id = request._request.GET['id']
            amount = Expenses.objects.filter(sheetId_id=pk).aggregate(Sum('amount'))
            expenses = Expenses.objects.filter(sheetId_id=pk).count()
            return Response({"amount": amount['amount__sum'],"expenses":expenses})


class Detail(APIView):
    def get(self,request):
        if request.method == 'GET':
            pk = request._request.GET['pk']
            persons= Persons.objects.filter(sheetId_id=pk).values_list("id")
            out = [item for t in persons for item in t]
            print(out)
            new = []
            for item in out:
                amount = Expenses.objects.filter(sheetId_id=pk, paidBy_id=item).aggregate(Sum('amount'))
                expenses = Persons.objects.filter(sheetId_id=pk, id=item).values("nickname").distinct()
                expensesPay = Expenses.objects.filter(sheetId_id=pk, paidBy_id=item).count()
                new.append("item="+str(item)+","+"amount="+ str(amount['amount__sum'])+ ","+"expensesPay="+str(expensesPay)+","+"paidBy="+expenses[0]['nickname'])
            print(new)
            return Response(new)


class AllExpense(APIView):
    def get(self, request):
        if request.method == 'GET':
            pk = request._request.GET['pk']
            expenses = Expenses.objects.filter(sheetId_id=pk).values_list("date", "description", "paidBy__nickname",
                                                                          "amount", "paidTo", "id").order_by('date')
            if expenses:
                return Response(expenses)
            else:
                return Response("NO DATA FOUND", status=status.HTTP_204_NO_CONTENT)


