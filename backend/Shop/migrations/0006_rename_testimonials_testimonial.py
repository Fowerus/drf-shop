# Generated by Django 3.2.2 on 2021-05-11 08:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Shop', '0005_alter_product_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Testimonials',
            new_name='Testimonial',
        ),
    ]
