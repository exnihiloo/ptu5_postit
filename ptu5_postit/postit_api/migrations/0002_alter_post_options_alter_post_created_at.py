# Generated by Django 4.1.3 on 2022-11-24 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postit_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
    ]