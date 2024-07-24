from django import forms

from books.models import Favorite, Rating, Book, Genre, Reviews


class BookForm(forms.ModelForm):
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(),
                                    label='Жанр', help_text='Выберите жанр!',
                                    widget=forms.widgets.Select(attrs={'size': 8}))

    class Meta:
        model = Book
        fields = ['title', 'description', 'price', 'cover_image', 'genre', 'tags']

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super().__init__(*args, **kwargs)
        self.fields['cover_image'].widget.attrs.update({'id': 'cover_image_id'})


class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['book']
        widgets = {
            'book': forms.HiddenInput()
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['text']
