from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.deletes()
Book.objects.all()
# <QuerySet []>
