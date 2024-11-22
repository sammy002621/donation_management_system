# Generated by Django 5.1.3 on 2024-11-21 09:05

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('donors', '0001_initial'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donation_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('bank_transfer', 'Bank Transfer'), ('check', 'Check')], max_length=20)),
                ('donation_date', models.DateTimeField(auto_now_add=True)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('receipt_generated', models.BooleanField(default=False)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donors.donor')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
            options={
                'ordering': ['-donation_date'],
            },
        ),
    ]