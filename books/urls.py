from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),

    # Корзина
    path('<int:book_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/item/<int:cart_item_id>/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/item/<int:cart_item_id>/update/', views.update_cart_item, name='update_cart_item'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/checkout/', views.checkout_order, name='checkout_order'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

    # Электронные книги и учебный баланс
    path('balance/top-up/', views.top_up_balance, name='top_up_balance'),
    path('<int:book_id>/buy-ebook/', views.buy_ebook, name='buy_ebook'),
    path('<int:book_id>/read/', views.read_ebook, name='read_ebook'),

    # Список желаний
    path('<int:book_id>/add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('<int:book_id>/remove-from-wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),

    # Статус прочтения
    path('<int:book_id>/toggle-read/', views.toggle_read_status, name='toggle_read_status'),

    # Отзывы
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]

