# Generated by Django 4.1.7 on 2023-03-20 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_product_image_productattribute_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='image',
            field=models.ImageField(null=True, upload_to='product_imgs/'),
        ),
    ]
