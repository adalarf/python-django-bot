# Generated by Django 4.2.11 on 2024-03-21 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_alter_card_card_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="favorite_users",
            field=models.ManyToManyField(blank=True, to="app.user"),
        ),
    ]