# Generated by Django 4.0.4 on 2023-07-18 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('price_t', '0003_delete_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=50)),
                ('product_url', models.URLField(unique=True)),
                ('product_price', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=50)),
            ],
        ),
    ]
