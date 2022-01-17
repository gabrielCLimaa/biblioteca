from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from catalog.forms import RenewBookForm
import datetime

# Create your views here.

def index(request):
    num_books = Book.objects.count()
    num_books_instance = BookInstance.objects.count()
    num_available_books = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    num_visitors = request.session.get('num_visitors', 0)
    request.session['num_visitors'] = num_visitors + 1

    context = {
        'num_books' : num_books,
        'num_authors' : num_authors,
        'num_books_instance' : num_books_instance,
        'num_available_books' : num_available_books,
        'num_visitors' : num_visitors
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book

class BookDetails(generic.DetailView):
    model = Book

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model: BookInstance
    template_name = 'catalog/loaned_books_user.html'

    def get_queryset(self):
        return BookInstance.objects.filter(user=self.request.user).filter(status__exact='o').order_by('due_back')



@permission_required('catalog.can_renew_loan')
def book_renew_loan(request, pk):
    
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':

        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('mybooks') )

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_loan.html', context)