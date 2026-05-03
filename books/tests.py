from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book, Author, Genre, Cart, CartItem, Wishlist, Review

class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.genre = Genre.objects.create(name="Test Genre")
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            description="Test description",
            price=100
        )
        self.book.genres.add(self.genre)

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author.name, "Test Author")
        self.assertEqual(self.book.price, 100)

class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.book = Book.objects.create(title="Test Book", author=Author.objects.create(name="Author"), price=50)

    def test_add_to_cart(self):
        cart, created = Cart.objects.get_or_create(user=self.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=self.book, quantity=2)
        self.assertEqual(cart_item.total_price(), 100)

class WishlistTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.book = Book.objects.create(title="Test Book", author=Author.objects.create(name="Author"), price=50)

    def test_add_to_wishlist(self):
        wishlist, created = Wishlist.objects.get_or_create(user=self.user)
        wishlist.books.add(self.book)
        self.assertIn(self.book, wishlist.books.all())

class HomePageTest(TestCase):
    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
