# Generated by Django 4.1.13 on 2024-03-28 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_vendor_remove_expenses_vendors_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lead',
            options={'verbose_name': 'Lead', 'verbose_name_plural': 'Leads'},
        ),
        migrations.RemoveField(
            model_name='lead',
            name='convert',
        ),
        migrations.AddField(
            model_name='lead',
            name='converted',
            field=models.BooleanField(default=False, verbose_name='Converted'),
        ),
        migrations.AddField(
            model_name='lead',
            name='referral',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Referral'),
        ),
        migrations.AlterField(
            model_name='event',
            name='mode_of_payment',
            field=models.CharField(choices=[('cash', 'Cash'), ('cheque', 'Cheque'), ('online', 'Online'), ('not_yet_decided', 'Not Yet Decided')], default='not_yet', max_length=20),
        ),
        migrations.AlterField(
            model_name='event',
            name='type_of_event',
            field=models.CharField(choices=[('conference', 'Conference'), ('seminar', 'Seminar'), ('workshop', 'Workshop'), ('meeting', 'Meeting'), ('party', 'Party'), ('marriage', 'Marriage'), ('haldi', 'Haldi'), ('mehendi', 'Mehendi'), ('baby_shower', 'Baby Shower'), ('other', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='payment_status',
            field=models.CharField(choices=[('received', 'Received'), ('not_received', 'Not Received'), ('partial_payment', 'Partial Payment')], default='not_paid', max_length=20),
        ),
        migrations.AlterField(
            model_name='lead',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='dashboard.client', verbose_name='Client'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='message',
            field=models.TextField(verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='reject',
            field=models.BooleanField(default=False, verbose_name='Rejected'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='source',
            field=models.CharField(choices=[('online', 'Online'), ('offline', 'Offline')], max_length=10, verbose_name='Source'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User who created the lead'),
        ),
        migrations.AlterField(
            model_name='sales',
            name='payment_status',
            field=models.CharField(choices=[('received', 'Received'), ('not_received', 'Not Received'), ('partial_payment', 'Partial Payment')], default='not_yet', max_length=20),
        ),
    ]
