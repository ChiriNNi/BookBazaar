from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from basket.models import Basket
from books.models import Book


def basket(request):
    baskets = Basket.objects.filter(user=request.user)
    context = {'baskets': baskets}
    return render(request, 'basket/basket.html', context)


@login_required
def basket_add(request, book_id):
    book = Book.objects.get(id=book_id)
    baskets = Basket.objects.filter(user=request.user, book=book)

    if not baskets.exists():
        Basket.objects.create(user=request.user, book=book, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])