from django.urls import path
from .views import BookListCreateAPIView, BookDetailAPIView, BookSearchView, BorrowBookView, LoanDetailView, LoanListView, MemberDetailAPIView, MemberListCreateAPIView, ReturnBookView
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({"message": "Welcome to the Library Management System!"})


urlpatterns = [
    path('api/books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('api/books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('api/books/search/', BookSearchView.as_view(), name='book-search'),
    path('api/members/', MemberListCreateAPIView.as_view(), name='member-list-create'),
    path('api/members/<int:pk>/', MemberDetailAPIView.as_view(), name='member-detail'),
    path('api/loans/borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('api/loans/return/', ReturnBookView.as_view(), name='return-book'),
    path('api/loans/', LoanListView.as_view(), name='loan-list'),
    path('api/loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),
    path('', root_view, name='root-view'),
]
