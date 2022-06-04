# Generated by Django 2.2.28 on 2022-06-03 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('PokedexCreature', '0003_remove_pokedexcreature_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('trainer_id', models.IntegerField()),
                ('surname', models.CharField(max_length=255)),
                ('level', models.IntegerField()),
                ('experience', models.IntegerField()),
                ('pokedex_creature_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PokedexCreature.PokedexCreature')),
            ],
        ),
    ]