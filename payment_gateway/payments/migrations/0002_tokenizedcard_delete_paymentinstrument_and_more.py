# Generated by Django 5.2 on 2025-04-13 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenizedCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_code', models.CharField(blank=True, max_length=100, null=True)),
                ('token', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('scheme', models.CharField(blank=True, max_length=50, null=True)),
                ('bin', models.CharField(blank=True, max_length=6, null=True)),
                ('last4', models.CharField(blank=True, max_length=4, null=True)),
                ('expiry_month', models.CharField(blank=True, max_length=2, null=True)),
                ('expiry_year', models.CharField(blank=True, max_length=4, null=True)),
                ('customer_code', models.CharField(blank=True, max_length=100, null=True)),
                ('brand_type', models.CharField(blank=True, max_length=50, null=True)),
                ('brand_category', models.CharField(blank=True, max_length=50, null=True)),
                ('merchant_reference', models.CharField(blank=True, max_length=255, null=True)),
                ('save_card_for_future', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('is_new', models.BooleanField(default=True)),
            ],
        ),
        migrations.DeleteModel(
            name='PaymentInstrument',
        ),
        migrations.AlterField(
            model_name='cardholderdetail',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='cardholderdetail',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cardholderdetail',
            name='frequent_flyer_number',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='cardholderdetail',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cardholderdetail',
            name='ref_title',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cardholderdetail',
            name='title',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='cardtokenrequest',
            name='card_holder_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.cardholderdetail'),
        ),
        migrations.AlterField(
            model_name='cardtokenrequest',
            name='instrument',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='cardtokenrequest',
            name='save_for_future',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cardtokenrequest',
            name='scheme',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='fraudcheckresult',
            name='provider_reference_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='fraudcheckresult',
            name='provider_response_message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='bank_transaction_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='customer_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='error_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='fraud_check_result',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.fraudcheckresult'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='fraud_check_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='gateway_response_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='gateway_response_message',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='merchant_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='payment',
            name='token',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='uicomponentrequest',
            name='client_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='uicomponentrequest',
            name='idempotency_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='uicomponentrequest',
            name='merchant_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='uicomponentrequest',
            name='order_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='uicomponentrequest',
            name='transaction_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='uicomponentrequest',
            name='ui_component_string',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tokenizedcard',
            name='card_holder_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payments.cardholderdetail'),
        ),
        migrations.AddField(
            model_name='tokenizedcard',
            name='card_token_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payments.cardtokenrequest'),
        ),
        migrations.AddField(
            model_name='tokenizedcard',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payments.payment'),
        ),
        migrations.AddField(
            model_name='tokenizedcard',
            name='ui_component_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payments.uicomponentrequest'),
        ),
        migrations.DeleteModel(
            name='TokenisedCard',
        ),
    ]
