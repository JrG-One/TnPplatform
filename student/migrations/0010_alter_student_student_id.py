# Generated by Django 5.0.1 on 2024-02-12 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0009_remove_student_id_alter_student_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='Student_ID',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]