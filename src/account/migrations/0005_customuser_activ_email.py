# Generated by Django 4.0.1 on 2022-01-17 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='activ_email',
            field=models.BooleanField(default=False),
        ),
    ]
