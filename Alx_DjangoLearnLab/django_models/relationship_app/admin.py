from django.contrib import admin
from .models import UserProfile, Book, Library, Librarian, Author

# 🔹 UserProfile Admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'role')


# 🔹 Book Admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'published_date', 'available')
    list_filter = ('available', 'published_date')
    search_fields = ('title', 'author')


# 🔹 Library Admin
@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# 🔹 Librarian Admin
@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'library', 'user', 'role')
    list_filter = ('role', 'library')
    search_fields = ('name', 'user__username')


# 🔹 Author Admin
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
