from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # عرض الأعمدة
    list_filter = ('publication_year', 'author')            # فلترة حسب السنة أو المؤلف
    search_fields = ('title', 'author')                     # البحث داخل العنوان والمؤلف

admin.site.register(Book, BookAdmin)
