from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    description = models.TextField()
    preview_text = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    def average_rating(self):
        average = self.reviews.aggregate(models.Avg('rating'))['rating__avg']
        return round(average, 1) if average else 0


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.total_price()
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.book.title}"

    def total_price(self):
        return self.quantity * self.book.price


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    books = models.ManyToManyField(Book, related_name='wishlisted_by')

    def __str__(self):
        return f"Wishlist of {self.user.username}"


class ReadStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='read_statuses')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='read_statuses')
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'book']
        verbose_name = 'Статус прочтения'
        verbose_name_plural = 'Статусы прочтения'

    def __str__(self):
        return f"{self.book.title} — {'Прочитано' if self.is_read else 'Не прочитано'} для {self.user.username}"


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    RATING_CHOICES = [(i, '★' * i + '☆' * (10 - i)) for i in range(1, 11)]

    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=10)
    comment = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['book', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.book.title}"

    def get_star_rating(self):
        return '★' * self.rating + '☆' * (10 - self.rating)