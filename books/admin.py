from django.contrib import admin
from .models import Author, Genre, Book, Cart, CartItem, Wishlist, Review, UserBalance, EbookPurchase, Order, OrderItem

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
    list_display = ['title', 'author', 'price', 'has_ebook', 'ebook_price']  # Убрали created_at
    list_filter = ['genres', 'has_ebook']  # Убрали created_at
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


@admin.register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount']
    search_fields = ['user__username']


@admin.register(EbookPurchase)
class EbookPurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'price', 'purchased_at']
    list_filter = ['purchased_at']
    search_fields = ['user__username', 'book__title']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'full_name', 'phone', 'address']
    inlines = [OrderItemInline]
