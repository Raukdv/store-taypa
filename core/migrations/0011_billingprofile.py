# Generated by Django 3.2.12 on 2022-03-24 19:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20220323_1421'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_payment', models.CharField(choices=[('paypal', 'Paypal'), ('stripe', 'Stripe'), ('culqui', 'Culqui')], max_length=50)),
                ('token', models.CharField(max_length=50)),
                ('card_id', models.CharField(max_length=50)),
                ('last4', models.CharField(max_length=4)),
                ('brand', models.CharField(max_length=10)),
                ('default', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
