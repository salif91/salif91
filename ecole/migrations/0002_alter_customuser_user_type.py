# Generated by Django 4.2.6 on 2024-01-16 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecole', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('admin', 'admin'), ('personnel', 'personnel'), ('etudiant', 'etudiant')], max_length=10),
        ),
    ]