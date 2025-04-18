# Generated by Django 5.2 on 2025-04-10 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('size', models.CharField(choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')], max_length=20)),
                ('temperature', models.FloatField()),
                ('sweetness', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Sandwich', 'Sandwich'), ('Burger', 'Burger'), ('Salad', 'Salad'), ('Durum', 'Durum')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Fruit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Apple', 'Apple'), ('Mango', 'Mango'), ('Orange', 'Orange'), ('Pitaya', 'Pitaya'), ('Grape', 'Grape')], max_length=20)),
            ],
        ),
    ]
