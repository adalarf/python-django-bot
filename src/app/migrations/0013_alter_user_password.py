# Generated by Django 4.2.11 on 2024-04-29 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0012_user_password_issuedtoken"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
