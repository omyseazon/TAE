# Generated by Django 4.0.2 on 2022-05-19 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TAEApp', '0005_complain1_complain2_alter_news_description2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complain1',
            name='ServiceType',
            field=models.CharField(choices=[('Kazi UAE', 'Kazi UAE'), ('Kununua Biashara', 'Kununua Biashara'), ('Matibabu', 'Matibabu'), ('Masomo', 'Masomo'), ('Mengine', 'Mengine')], max_length=50),
        ),
    ]
