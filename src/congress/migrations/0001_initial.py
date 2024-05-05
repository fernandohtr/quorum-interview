# Generated by Django 5.0.4 on 2024-05-05 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Legislator",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name="Bill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=250)),
                ("sponsor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="congress.legislator")),
            ],
        ),
        migrations.CreateModel(
            name="Vote",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("bill", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="congress.bill")),
            ],
        ),
        migrations.CreateModel(
            name="VoteResult",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("vote_type", models.IntegerField(choices=[(1, "Supportes"), (2, "Opposes")])),
                (
                    "legislator",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="congress.legislator"),
                ),
                ("vote", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="congress.vote")),
            ],
        ),
    ]