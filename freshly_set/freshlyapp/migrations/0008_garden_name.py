# Generated by Django 5.0.7 on 2024-07-21 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freshlyapp', '0007_garden_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='garden',
            name='name',
            field=models.CharField(default='DEFAULT VALUE', max_length=100),
        ),
    ]
