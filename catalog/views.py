from django.shortcuts import render
from django.views import generic
from .models import *

# Create your views here.

def index(request):

    num_books = Book.objects.count()
    num_books_instance = BookInstance.objects.count()

    num_available_books = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()

    context = {
        'num_books' : num_books,
        'num_authors' : num_authors,
        'num_books_instance' : num_books_instance,
        'num_available_books' : num_available_books
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book

class BookDetails(generic.DetailView):
    model = Book