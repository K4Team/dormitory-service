# Generated by Django 3.1.1 on 2020-09-10 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('mobile', models.IntegerField(max_length=20)),
                ('email', models.CharField(max_length=255)),
                ('income', models.IntegerField(max_length=20)),
                ('create_date', models.DateTimeField()),
            ],
        ),
    ]
