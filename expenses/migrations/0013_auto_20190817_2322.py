# Generated by Django 2.2 on 2019-08-17 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0012_auto_20190801_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
