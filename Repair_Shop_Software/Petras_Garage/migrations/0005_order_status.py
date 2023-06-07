# Generated by Django 4.2.1 on 2023-06-06 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Petras_Garage', '0004_order_due_to_finish_repair'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('processing', 'Processing'), ('complete', 'Complete'), ('cancelled', 'Cancelled')], db_index=True, default=0, max_length=20, verbose_name='Status'),
        ),
    ]
