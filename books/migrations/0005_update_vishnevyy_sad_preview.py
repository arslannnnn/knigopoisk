from django.db import migrations

LONG_PREVIEW = (
    "Сезон вишневой яблони начинался. Дом стоял на склоне, а слуги мечтали о том, как они будут продавать сад и уезжать в город. "
    "В большом зале звучали шаги, и каждый угол был наполнен запахом свежей краски и влажной земли из сада. "
    "Герои ощущали, что перемены уже близки, и старое имение скоро изменится навсегда."
)


def update_preview_text(apps, schema_editor):
    Book = apps.get_model('books', 'Book')
    book = Book.objects.filter(title='Вишнёвый сад').first()
    if book:
        book.preview_text = LONG_PREVIEW
        book.save()


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_fill_preview_text'),
    ]

    operations = [
        migrations.RunPython(update_preview_text, migrations.RunPython.noop),
    ]
