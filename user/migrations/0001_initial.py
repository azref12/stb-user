# Generated by Django 3.2.6 on 2022-06-13 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('reward', models.IntegerField(default=0)),
                ('point', models.IntegerField(default=0)),
                ('coin', models.IntegerField(default=0)),
                ('phone_number', models.CharField(max_length=50)),
                ('app_id', models.IntegerField(default=0)),
                ('pin', models.IntegerField(default=0)),
                ('code', models.IntegerField(default=0)),
            ],
        ),
    ]
