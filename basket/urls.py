from django.urls import path

from .views import basket, basket_add, basket_remove

app_name = 'baskets'

urlpatterns = [
    path('', basket, name='basket'),
    path('add/<int:book_id>/', basket_add, name='basket_add'),
    path('remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
