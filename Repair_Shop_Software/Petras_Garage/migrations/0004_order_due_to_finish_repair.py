# Generated by Django 4.2.1 on 2023-06-06 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Petras_Garage', '0003_remove_vehicle_client_vehicle_note_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='due_to_finish_repair',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='Due to finish repair'),
        ),
    ]
