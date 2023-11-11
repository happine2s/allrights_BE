# Generated by Django 4.2.7 on 2023-11-11 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0013_merge_20231110_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='length',
            field=models.CharField(choices=[('short', '1분 이내'), ('medium', '1~5분'), ('long', '5분 이상')], max_length=10),
        ),
    ]
