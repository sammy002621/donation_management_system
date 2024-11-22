# Generated by Django 5.1.3 on 2024-11-21 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('location', models.CharField(max_length=200)),
                ('donation_goal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, upload_to='event_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
