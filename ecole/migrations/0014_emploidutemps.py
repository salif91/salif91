# Generated by Django 4.2.6 on 2024-02-19 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecole', '0013_alter_etudiant_numero_matricule'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmploiDuTemps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heure_debut', models.TimeField()),
                ('heure_fin', models.TimeField()),
                ('jour', models.CharField(max_length=50)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecole.classe')),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecole.matiere')),
            ],
        ),
    ]
