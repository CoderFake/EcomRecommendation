# Generated by Django 5.0.6 on 2024-05-15 00:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0018_remove_account_is_login"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="is_login",
            field=models.BooleanField(default=False),
        ),
    ]