# Generated by Django 3.2.2 on 2021-05-16 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Shop', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='in_order',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_code', models.CharField(max_length=70, verbose_name='hash_code')),
                ('url', models.CharField(max_length=200, verbose_name='url')),
                ('order_code', models.IntegerField()),
                ('paid', models.BooleanField(default=False)),
                ('date_creating', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_cart_orders', to=settings.AUTH_USER_MODEL, verbose_name='Orders')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ['-date_creating'],
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creating', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups_order', to='Shop.order', verbose_name='order_id')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_in_groups', to='Shop.product', verbose_name='Groups')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_cart_groups', to=settings.AUTH_USER_MODEL, verbose_name='Groups')),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
                'ordering': ['-date_creating'],
            },
        ),
    ]
