# Generated by Django 3.2.2 on 2021-05-11 09:08

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='../static/Users/images/default-user-image.jpeg', force_format=None, keep_meta=True, quality=0, size=[225, 225], upload_to='./static/Users/images', verbose_name='image'),
        ),
    ]
