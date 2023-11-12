# Generated by Django 4.2.5 on 2023-10-23 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('IDPublicacion', models.AutoField(primary_key=True, serialize=False)),
                ('Titulo', models.CharField(max_length=200)),
                ('FechaPublicacion', models.DateField(auto_now_add=True)),
                ('Contenido', models.CharField(max_length=5000)),
                ('FechaNoticia', models.DateField()),
                ('Imagen', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'Publicacion',
            },
        ),
        migrations.CreateModel(
            name='Recinto',
            fields=[
                ('IDRecinto', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=100)),
                ('Direccion', models.CharField(max_length=150)),
                ('Telefono', models.PositiveIntegerField(null=True)),
                ('Horario', models.CharField(max_length=45)),
                ('Imagen', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'Recinto',
            },
        ),
    ]