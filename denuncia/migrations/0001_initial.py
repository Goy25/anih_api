# Generated by Django 4.2.5 on 2023-10-08 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('IDCategoria', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Categoria',
            },
        ),
    ]
