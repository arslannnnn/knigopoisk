from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Book, Cart, CartItem, Wishlist, Genre, Review, ReadStatus
from .forms import ReviewForm


def book_list(request):
    genre_filter = request.GET.get('genre', '')
    if genre_filter:
        books = Book.objects.filter(genres__name=genre_filter)
    else:
        books = Book.objects.all()

    books = books.annotate(avg_rating=Avg('reviews__rating'))
    all_genres = Genre.objects.all()

    return render(request, 'books/book_list.html', {
        'books': books,
        'selected_genre': genre_filter,
        'all_genres': all_genres
    })


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all().order_by('-created_at')

    avg_rating = book.reviews.aggregate(Avg('rating'))['rating__avg']
    if avg_rating:
        avg_rating = round(avg_rating, 1)
        avg_rating_percent = int(avg_rating * 10)
    else:
        avg_rating = 0
        avg_rating_percent = 0
    review_count = reviews.count()

    user_review = None
    in_wishlist = False
    read_status = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(book=book, user=request.user).first()
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist:
            in_wishlist = book in wishlist.books.all()
        read_status = ReadStatus.objects.filter(book=book, user=request.user).first()

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            existing_review = Review.objects.filter(book=book, user=request.user).first()
            if existing_review:
                existing_review.rating = form.cleaned_data['rating']
                existing_review.comment = form.cleaned_data['comment']
                existing_review.save()
                messages.success(request, 'Ваш отзыв обновлен!')
            else:
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('book_detail', book_id=book_id)
    else:
        if user_review:
            form = ReviewForm(instance=user_review)
        else:
            form = ReviewForm()

    return render(request, 'books/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'avg_rating_percent': avg_rating_percent,
        'review_count': review_count,
        'form': form,
        'user_review': user_review,
        'in_wishlist': in_wishlist,
        'read_status': read_status,
    })


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'Книга "{book.title}" добавлена в корзину!')
    return redirect('book_detail', book_id=book_id)


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    book_title = cart_item.book.title
    cart_item.delete()
    messages.success(request, f'Книга "{book_title}" удалена из корзины!')
    return redirect('view_cart')


@login_required
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Количество обновлено!')
        else:
            cart_item.delete()
            messages.success(request, 'Книга удалена из корзины!')
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    total = 0
    for item in cart.items.all():
        total += item.total_price()
    return render(request, 'books/cart.html', {
        'cart': cart,
        'total_price': total
    })


@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.books.add(book)
    messages.success(request, f'Книга "{book.title}" добавлена в список желаний!')
    return redirect('book_detail', book_id=book_id)


@login_required
def remove_from_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.books.remove(book)
    messages.success(request, f'Книга "{book.title}" удалена из списка желаний!')
    return redirect('view_wishlist')


@login_required
def view_wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'books/wishlist.html', {
        'wishlist': wishlist
    })


@login_required
def toggle_read_status(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        status, _ = ReadStatus.objects.get_or_create(user=request.user, book=book)
        status.is_read = not status.is_read
        status.save()
        messages.success(
            request,
            f"Книга \"{book.title}\" помечена как {'прочитано' if status.is_read else 'не прочитано'}"
        )
    return redirect('book_detail', book_id=book_id)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book_id = review.book.id
    review.delete()
    messages.success(request, 'Ваш отзыв удален!')
    return redirect('book_detail', book_id=book_id)