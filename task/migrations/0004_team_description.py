# Generated by Django 4.2.5 on 2023-10-02 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_taskpoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='description',
            field=models.CharField(max_length=127, null=True),
        ),
    ]
