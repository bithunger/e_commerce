# Generated by Django 4.1.7 on 2023-04-19 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='address',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='email',
            field=models.CharField(default=None, max_length=150),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='mobile',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='name',
            field=models.CharField(default=None, max_length=150),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='tran_id',
            field=models.CharField(default=None, max_length=150),
        ),
    ]
