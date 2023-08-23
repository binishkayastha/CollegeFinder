# Generated by Django 4.2.4 on 2023-08-23 10:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('colleges', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='college',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='college',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='college',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]