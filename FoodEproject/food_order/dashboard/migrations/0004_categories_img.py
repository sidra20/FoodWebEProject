# Generated by Django 4.1.3 on 2022-11-16 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_categories_foodtypes_alter_users_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='img',
            field=models.ImageField(default=None, upload_to='images/'),
        ),
    ]