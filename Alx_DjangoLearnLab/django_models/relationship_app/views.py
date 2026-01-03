from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Book, Library
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book




def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def book_list(request):
    """Retrieves all books and renders a template displaying the list."""
    books = Book.objects.all()  # Fetch all book instances from the database
    context = {'book_list': books}  # Create a context dictionary with book list
    return render(request, 'books/book_list.html', context)

class BookDetailView(DetailView):
    """A class-based view for displaying details of a specific book."""
    model = Book
    template_name = 'books/book_detail.html'

    def get_context_data(self, **kwargs):
        """Injects additional context data specific to the book."""
        context = super().get_context_data(**kwargs)  # Get default context data
        book = self.get_object()  # Retrieve the current book instance
        context['average_rating'] = book.get_average_rating()
        return context
    
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def librarian_dashboard(request):
    return render(request, 'librarian_dashboard.html')


def member_dashboard(request):
    return render(request, 'member_dashboard.html')


@permission_required('relationship_app.can_add_book')
def add_book(request):
    # كود إضافة كتاب جديد
    return render(request, 'add_book.html')

@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    # كود تعديل كتاب
    return render(request, 'edit_book.html')

@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    # كود حذف كتاب
    return render(request, 'delete_book.html')


# عرض قائمة الكتب
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

# إضافة كتاب جديد (يتطلب صلاحية can_add_book)
@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')
        Book.objects.create(title=title, author=author, published_date=published_date)
        return redirect('book_list')
    return render(request, 'add_book.html')

# تعديل كتاب (يتطلب صلاحية can_change_book)
@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.published_date = request.POST.get('published_date')
        book.save()
        return redirect('book_list')
    return render(request, 'edit_book.html', {'book': book})

# حذف كتاب (يتطلب صلاحية can_delete_book)
@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'delete_book.html', {'book': book})


