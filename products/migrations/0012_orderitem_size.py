# Generated by Django 5.2 on 2025-04-15 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_order_name_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
