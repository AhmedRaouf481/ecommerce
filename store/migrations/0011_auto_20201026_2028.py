# Generated by Django 3.1.2 on 2020-10-26 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
