# Generated by Django 4.1.7 on 2023-02-25 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0003_lead_team'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lead',
            options={'ordering': ('-created_at',)},
        ),
    ]
