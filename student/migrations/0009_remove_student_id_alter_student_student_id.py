# Generated by Django 5.0.1 on 2024-02-12 18:23

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_alter_student_student_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='id',
        ),
        migrations.AlterField(
            model_name='student',
            name='Student_ID',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]