# Generated by Django 5.0.6 on 2024-08-19 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0010_category_description"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ["id"]},
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
    ]
