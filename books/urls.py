from django.urls import path
from .views import index, filtered_books_with_genre, book_detail, add_to_favorites, book_list, FavoriteListView, add_book, rate_book, AddReview


app_name = 'books'

urlpatterns = [
    path('', index, name='index'),
    path('books/genre/<int:genre_id>/', filtered_books_with_genre, name='filter'),
    path('books/detail/<int:book_id>/', book_detail, name='book_detail'),
    path('books/add_to_favorites/', add_to_favorites, name='add_to_favorites'),
    path('books/favorites/', FavoriteListView.as_view(), name='favorites'),
    path('books/all/', book_list, name='books'),
    path('books/rate/<int:book_id>/', rate_book, name='rate_book'),
    path('books/add/', add_book, name='add_book'),
    path('books/review/<int:pk>/', AddReview.as_view(), name='add_review'),
]
