import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_ebooks_balance_and_chekhov'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=30)),
                ('address', models.TextField()),
                ('comment', models.TextField(blank=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('status', models.CharField(choices=[('processing', 'Оформлен'), ('in_transit', 'В пути'), ('delivered', 'Доставлен')], default='in_transit', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='books.order')),
            ],
        ),
    ]
