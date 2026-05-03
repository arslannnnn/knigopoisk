# Generated manually to support preview text and read status features

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0002_alter_author_options_alter_book_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="preview_text",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="ReadStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_read", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="read_statuses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="read_statuses",
                        to="books.book",
                    ),
                ),
            ],
        ),
    ]
