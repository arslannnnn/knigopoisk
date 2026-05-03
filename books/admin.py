from django.contrib import admin
from .models import Author, Genre, Book, Cart, CartItem, Wishlist, Review

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']  # ТОЛЬКО name
    search_fields = ['name']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price']  # Убрали created_at
    list_filter = ['genres']  # Убрали created_at
    search_fields = ['title', 'author__name']
    filter_horizontal = ['genres']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user']  # ТОЛЬКО user

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'book', 'quantity']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user']  # ТОЛЬКО user
    filter_horizontal = ['books']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'user__username', 'comment']