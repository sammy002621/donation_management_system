# Generated by Django 5.1.3 on 2024-11-21 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='is_active',
        ),
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('completed', 'Completed')], default='upcoming', max_length=10),
        ),
        migrations.AddField(
            model_name='event',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='events/'),
        ),
    ]