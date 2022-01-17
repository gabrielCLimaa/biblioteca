from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Genero, exemplo: Comedia...")

    def getName(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200, help_text="Linguagem, exemplo: Portugues...")

    def getName(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    day_of_birth = models.DateField(null=True, blank=True)
    day_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
    
    def getName(self):
        return f'{self.first_name} {self.last_name}'

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000,help_text="Descrição")
    isbn = models.CharField('ISBN',max_length=13)
    genre = models.ManyToManyField(Genre, help_text="Selecione um genero")
    language = models.ForeignKey(Language, on_delete=models.SET_NULL,null=True)

    def getAbsolutPath(self):
        return reverse('book_details', args=[str(self.id)])

    def getTitle(self):
        return self.title

    def getCompleteInfo(self):
         return f'{self.title}, {self.author}, {self.summary}, {self.isbn}, {self.genre}, {self.language}'

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, help_text="Identificador")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    published_by = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_renew_loan", "Pode renovar emprestimo"),)

    @property
    def isLate(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def getTitle(self):
        return self.book.title

    def getCompleteInfo(self):
         return f'{self.id}, {self.book.title}, {self.published_by}, {self.due_back}'