# Generated by Django 5.0.2 on 2024-02-08 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_alter_student_access_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='Access_Token',
            field=models.CharField(default='token', max_length=300),
            preserve_default=False,
        ),
    ]
