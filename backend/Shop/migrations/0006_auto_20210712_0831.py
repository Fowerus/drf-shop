# Generated by Django 3.2.2 on 2021-07-12 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0005_alter_currency_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['-date_creating'], 'verbose_name': 'Carts product', 'verbose_name_plural': 'Carts products'},
        ),
        migrations.AlterField(
            model_name='group',
            name='date_creating',
            field=models.DateTimeField(auto_now=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_creating',
            field=models.DateTimeField(auto_now=True, verbose_name='Date'),
        ),
    ]