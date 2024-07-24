from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from books.models import Book, Genre, Favorite, Rating, Author, Tag
from books.forms import BookForm, RatingForm, ReviewForm


def index(request):
    books = Book.objects.all().order_by('-created_date')[:8]
    genres = Genre.objects.all()
    context = {
        'books': books, 'genres': genres
    }
    return render(request, 'index.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_rating = None
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, book=book).exists()
        user_rating = Rating.objects.filter(book=book, user=request.user).first()

    if request.method == 'POST' and request.user.is_authenticated:
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.update_or_create(
                book=book,
                user=request.user,
                defaults={'score': form.cleaned_data['score']}
            )
            return redirect('books:book_detail', book_id=book_id)
    else:
        form = RatingForm()

    current_rating = Rating.objects.filter(book=book, user=request.user).first()
    rating_value = current_rating.score if current_rating else None
    rating_range = range(1, 6)

    context = {
        'book': book,
        'form': form,
        'is_favorite': is_favorite,
        'average_rating': book.get_average_rating(),
        'rating_count': book.get_rating_count(),
        'user_rating': user_rating,
        'rating_value': rating_value,
        'rating_range': rating_range,
    }
    return render(request, 'book_detail.html', context)


@login_required
def rate_book(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        score = int(request.POST.get('score', 0))

        # Handle existing rating
        rating, created = Rating.objects.update_or_create(
            book=book,
            user=request.user,
            defaults={'score': score}
        )

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


def filtered_books_with_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    books = Book.objects.filter(genre=genre)
    genres = Genre.objects.all()
    context = {
        'books': books,
        'genres': genres,
        'active_genre': genre,
    }
    return render(request, 'index.html', context)


@login_required
@require_POST
def add_to_favorites(request):
    book_id = request.POST.get('book_id')
    book = get_object_or_404(Book, id=book_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
    if not created:
        favorite.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


def book_list(request):
    selected_authors = request.GET.getlist('author')
    selected_tags = request.GET.getlist('tag')
    selected_genres = request.GET.getlist('genre')

    books = Book.objects.all()
    if selected_authors:
        books = books.filter(author__id__in=selected_authors)
    if selected_tags:
        books = books.filter(tags__id__in=selected_tags).distinct()
    if selected_genres:
        books = books.filter(genre__id__in=selected_genres).distinct()  # Исправлено на genre

    authors = Author.objects.all()
    tags = Tag.objects.all()
    genres = Genre.objects.all()

    context = {
        'books': books,
        'authors': authors,
        'tags': tags,
        'genres': genres,
        'selected_authors': selected_authors,
        'selected_tags': selected_tags,
        'selected_genres': selected_genres,
    }
    return render(request, 'book_list.html', context)


class FavoriteListView(ListView):
    model = Favorite
    template_name = 'favorites.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('book')


@login_required
def add_book(request):
    author = get_object_or_404(Author, first_name=request.user.first_name, last_name=request.user.last_name)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, author=author)
        if form.is_valid():
            book = form.save(commit=False)
            book.author = author
            book.save()
            form.save_m2m()
            return redirect('books:book_detail', book_id=book.id)
    else:
        form = BookForm(author=author)

    context = {
        'form': form
    }
    return render(request, 'add_book.html', context)


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        book = get_object_or_404(Book, id=pk)
        if form.is_valid():
            review = form.save(commit=False)
            if request.POST.get("parent", None):
                review.parent_id = int(request.POST.get("parent"))
            review.book = book
            review.user = request.user
            review.save()
            print("Review saved successfully!")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            print("Form errors:", form.errors)
            return HttpResponse(status=400)