# Generated by Django 5.1.1 on 2024-09-29 04:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="orderproduct",
            old_name="orden",
            new_name="order",
        ),
    ]