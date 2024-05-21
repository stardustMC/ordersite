# Generated by Django 3.2 on 2024-05-04 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20240505_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='creator',
            field=models.ForeignKey(limit_choices_to={'active': 1}, on_delete=django.db.models.deletion.CASCADE, to='web.administrator', verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='prior',
            field=models.ForeignKey(limit_choices_to={'active': 1}, on_delete=django.db.models.deletion.CASCADE, to='web.prior', verbose_name='等级'),
        ),
    ]
