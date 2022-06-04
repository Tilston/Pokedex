# Generated by Django 2.2.28 on 2022-06-03 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PokedexCreature',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('type1', models.CharField(max_length=255)),
                ('type2', models.CharField(max_length=255)),
                ('total', models.IntegerField()),
                ('hp', models.IntegerField()),
                ('attack', models.IntegerField()),
                ('defense', models.IntegerField()),
                ('sp_attack', models.IntegerField()),
                ('sp_defense', models.IntegerField()),
                ('speed', models.IntegerField()),
                ('generation', models.IntegerField()),
                ('legendary', models.BooleanField()),
            ],
        ),
    ]
