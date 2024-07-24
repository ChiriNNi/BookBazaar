from django.contrib import admin

from books.models import Genre, Author, Book, Favorite, Reviews, Tag

admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Favorite)
admin.site.register(Reviews)
admin.site.register(Tag)