# Generated by Django 5.2 on 2025-04-15 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(default=2, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='in_progress', max_length=20),
        ),
    ]
