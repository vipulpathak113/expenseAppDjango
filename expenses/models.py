import datetime

from django.db import models
from django.db.models import CharField
from django_mysql.models import ListCharField


class SheetData(models.Model):
    id = models.AutoField(primary_key=True)
    display_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    created_date = models.DateTimeField(default=datetime.datetime.now)


class Persons(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    nickname = models.CharField(max_length=200, blank=True, null=True,unique=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(default=datetime.datetime.now)
    sheetId = models.ForeignKey(SheetData, on_delete=models.CASCADE)


class Expenses(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    paidBy = models.ForeignKey(Persons, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)
    paidTo = ListCharField(
        base_field=CharField(max_length=500, blank=True, null=True), max_length=50
    )

    sheetId = models.ForeignKey(SheetData, on_delete=models.CASCADE, null=True, blank=True)


class Compute(models.Model):
    id = models.AutoField(primary_key=True)
    sheetId = models.ForeignKey(SheetData, on_delete=models.CASCADE)
    paidBy = models.ForeignKey(Persons, on_delete=models.CASCADE)
    owes = models.IntegerField(blank=True, null=True)
    owed = models.IntegerField(blank=True, null=True)
    owedTo=models.ForeignKey(Expenses, on_delete=models.CASCADE)



