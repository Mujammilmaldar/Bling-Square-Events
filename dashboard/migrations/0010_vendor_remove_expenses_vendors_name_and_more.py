# Generated by Django 4.1.13 on 2024-03-28 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_remove_attendance_convert_lead_convert'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('organization_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='expenses',
            name='vendors_name',
        ),
        migrations.RemoveField(
            model_name='expenses',
            name='vendors_organisation_name',
        ),
        migrations.AlterField(
            model_name='expenses',
            name='mode_of_payment',
            field=models.CharField(choices=[('cash', 'Cash'), ('cheque', 'Cheque'), ('online', 'Online'), ('not_yet_decided', 'Not Yet Decided')], default='not_yet_decided', max_length=20),
        ),
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('intern', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='expenses',
            name='vendor',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='dashboard.vendor'),
            preserve_default=False,
        ),
    ]
