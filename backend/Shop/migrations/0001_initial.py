# Generated by Django 3.2.2 on 2021-05-16 06:18

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creating', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Carts products',
                'ordering': ['-date_creating'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('date_creating', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['-date_creating'],
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='Name')),
                ('system_id', models.IntegerField(verbose_name='Id')),
                ('date_creating', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
            ],
            options={
                'verbose_name': 'Carrency',
                'verbose_name_plural': 'Carrencies',
                'ordering': ['-date_creating'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.CharField(max_length=1000, verbose_name='Description')),
                ('image', django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=0, size=[225, 225], upload_to='./static/Shop/images', verbose_name='Image')),
                ('cost', models.FloatField(verbose_name='Cost')),
                ('date_creating', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['-date_creating'],
            },
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars_count', models.IntegerField(verbose_name='Stars')),
                ('description', models.CharField(max_length=500, verbose_name='Description')),
                ('date_creating', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products_testimonials', to='Shop.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonials',
                'ordering': ['-date_creating'],
            },
        ),
    ]