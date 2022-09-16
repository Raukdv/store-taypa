# Generated by Django 3.2.12 on 2022-03-23 15:38

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_order_shipping_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='company',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.status'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='country',
            field=django_countries.fields.CountryField(blank=True, default='PE', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(editable=False, max_length=100, unique=True),
        ),
    ]