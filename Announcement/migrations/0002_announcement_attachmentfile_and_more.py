# Generated by Django 5.0.2 on 2024-03-11 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Announcement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='attachmentFile',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='announcement',
            name='attachmentLink',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
