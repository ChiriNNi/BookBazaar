from django.db import models

from books.models import Book
from users.models import User


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE)
    book = models.ForeignKey(verbose_name='Книга', to=Book, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина для {self.user.username} | Книга: {self.book.title}"

    def sum(self):
        return self.book.price * self.quantity



