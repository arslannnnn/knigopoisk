from decimal import Decimal

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def add_chekhov_ebook(apps, schema_editor):
    Author = apps.get_model('books', 'Author')
    Genre = apps.get_model('books', 'Genre')
    Book = apps.get_model('books', 'Book')

    author, _ = Author.objects.get_or_create(name='Антон Чехов')
    classic, _ = Genre.objects.get_or_create(name='Классика')
    story, _ = Genre.objects.get_or_create(name='Рассказ')

    book, _ = Book.objects.get_or_create(
        title='Дама с собачкой',
        author=author,
        defaults={
            'description': 'Короткий рассказ Антона Чехова о встрече Гурова и Анны Сергеевны в Ялте.',
            'preview_text': 'Говорили, что на набережной появилось новое лицо: дама с собачкой.',
            'price': Decimal('149.00'),
        },
    )
    book.description = 'Короткий рассказ Антона Чехова о встрече Гурова и Анны Сергеевны в Ялте.'
    book.preview_text = 'Говорили, что на набережной появилось новое лицо: дама с собачкой.'
    book.price = Decimal('149.00')
    book.has_ebook = True
    book.ebook_price = Decimal('99.00')
    book.ebook_file = 'books/ebook_texts/dama_s_sobachkoy.txt'
    book.save()
    book.genres.add(classic, story)


def remove_chekhov_ebook(apps, schema_editor):
    Book = apps.get_model('books', 'Book')
    Book.objects.filter(title='Дама с собачкой', author__name='Антон Чехов').delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0006_expand_all_preview_texts'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='ebook_file',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='book',
            name='ebook_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='book',
            name='has_ebook',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='UserBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='balance', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EbookPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchased_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ebook_purchases', to='books.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ebook_purchases', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-purchased_at'],
                'unique_together': {('user', 'book')},
            },
        ),
        migrations.RunPython(add_chekhov_ebook, remove_chekhov_ebook),
    ]
