# Generated by Django 5.0.7 on 2024-08-05 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_word_unique_word_in_dictionary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
