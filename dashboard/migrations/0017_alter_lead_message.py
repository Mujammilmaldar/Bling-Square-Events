# Generated by Django 4.1.13 on 2024-03-31 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_lead_sales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='message',
            field=models.TextField(blank=True, verbose_name='Message'),
        ),
    ]
