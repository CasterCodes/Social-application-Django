# Generated by Django 4.1 on 2022-12-28 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_postlikes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=255)),
                ('user', models.CharField(max_length=255)),
            ],
        ),
    ]
