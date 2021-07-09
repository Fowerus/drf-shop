# Generated by Django 3.2.2 on 2021-07-08 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default=1, max_length=150, verbose_name='first_name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default=1, max_length=150, verbose_name='last_name'),
            preserve_default=False,
        ),
    ]