# Generated by Django 4.0.2 on 2022-04-08 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TAEApp', '0002_rename_registeredstudent_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallery',
            name='PhotoURL',
        ),
        migrations.AlterField(
            model_name='gallery',
            name='Photo',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='member',
            name='Advice',
            field=models.TextField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='member',
            name='CompanyName',
            field=models.CharField(max_length=200, verbose_name='Company Name'),
        ),
    ]