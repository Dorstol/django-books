from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, DetailView

from .models import Book


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "book_list"
    login_url = "account_login"

    def get_queryset(self):
        title = self.request.GET.get("title")
        author = self.request.GET.get("author")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        return Book.objects.filter(
            Q(title__icontains=title), Q(author__icontains=author),
            Q(price__gte=min_price) | Q(price__lte=max_price)
        )


class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Book
    context_object_name = "book"
    template_name = "books/book_detail.html"
    login_url = "account_login"
    permission_required = "books.special_status"
    queryset = Book.objects.all().prefetch_related('reviews__author')


class SearchResultsListView(ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "books/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
