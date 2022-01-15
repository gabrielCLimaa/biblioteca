from django.shortcuts import render
from .models import *

# Create your views here.

def index(request):

    num_books = Book.objects.count()
    num_books_instance = BookInstace.objects.count()

    num_available_books = BookInstace.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()

    context = {
        'num_books' : num_books,
        'num_authors' : num_authors,
        'num_books_instance' : num_books_instance,
        'num_available_books' : num_available_books
    }

    return render(request, 'index.html', context=context)