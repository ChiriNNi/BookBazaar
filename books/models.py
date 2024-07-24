from django.db import models
from django.db.models import Avg

from users.models import User


class Genre(models.Model):
    """Жанры"""
    name = models.CharField(verbose_name='Жанр', max_length=128, unique=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.pk}/"

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Author(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    biography = models.TextField(verbose_name='Биография', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Tag(models.Model):
    """Теги"""
    name = models.CharField(max_length=30, verbose_name="Тег")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Book(models.Model):
    """Книги"""
    title = models.CharField(verbose_name="Название", max_length=256)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    price = models.DecimalField(verbose_name="Цена", max_digits=6, decimal_places=2)
    cover_image = models.ImageField(verbose_name='Обложка', upload_to='books-image/')
    genre = models.ForeignKey(verbose_name='Жанр', to=Genre, on_delete=models.CASCADE)
    author = models.ForeignKey(verbose_name='Автор', to=Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True)
    publication_year = models.PositiveIntegerField(verbose_name='Год издания', default=2024)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f"{self.title}"

    def get_average_rating(self):
        average = Rating.objects.filter(book=self).aggregate(Avg('score'))['score__avg']
        return round(average or 0, 1)

    def get_rating_count(self):
        return Rating.objects.filter(book=self).count()

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


#     def get_absolute_url(self):
#         return f"/detail/{self.pk}/"


class Favorite(models.Model):
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE)
    book = models.ForeignKey(verbose_name='Книга', to=Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    class Meta:
        unique_together = ('user', 'book')
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('user', 'book')
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, null=True, blank=True
    )
    book = models.ForeignKey(Book, verbose_name='Книга', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.book}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'