# Generated by Django 4.2.1 on 2023-10-05 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_delete_login_alter_emailvalidation_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailvalidation',
            name='attempt',
            field=models.CharField(default=3, max_length=5, null=True),
        ),
    ]