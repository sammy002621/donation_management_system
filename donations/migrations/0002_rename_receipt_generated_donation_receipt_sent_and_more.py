# Generated by Django 5.1.3 on 2024-11-21 09:37

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0001_initial'),
        ('events', '0002_remove_event_end_date_remove_event_is_active_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donation',
            old_name='receipt_generated',
            new_name='receipt_sent',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='donation_id',
        ),
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='donation',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.event'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='donation',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('check', 'Check'), ('credit_card', 'Credit Card'), ('bank_transfer', 'Bank Transfer')], max_length=20),
        ),
    ]
