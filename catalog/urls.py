from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetails.as_view(), name='book_details'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='mybooks'),
    path('book/<uuid:pk>/renew', views.book_renew_loan, name='book_renew_loan') 
]
