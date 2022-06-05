# Generated by Django 4.0.2 on 2022-06-05 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TAEApp', '0009_rename_electionapplicats_electionapplicant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=50)),
                ('Description1', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='FrontPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Photo', models.ImageField(upload_to='images')),
                ('Title', models.CharField(max_length=50)),
                ('Description1', models.TextField(max_length=200)),
                ('PublishDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
