from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from .models import Book, Loan, Member
from .serializers import BookSerializer, LoanSerializer, MemberSerializer
from datetime import timedelta
from django.utils.timezone import now


# List all books (public access) and create a new book (requires authentication)
class BookListCreateAPIView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

# Retrieve, update, or delete a specific book (requires authentication for update/delete)
class BookDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

class BookSearchView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title', None)
        author = self.request.query_params.get('author', None)
        genre = self.request.query_params.get('genre', None)

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if genre:
            queryset = queryset.filter(genre__icontains=genre)

        return queryset

# List and Create Members
class MemberListCreateAPIView(ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

# Retrieve, Update, Delete a Specific Member
class MemberDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]  # No authentication required for GET
        return [permissions.IsAuthenticated()]

# Borrow a Book
class BorrowBookView(CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        book_id = request.data.get('book_id')
        member_id = request.data.get('member_id')

        # Validate book and member existence
        try:
            book = Book.objects.get(id=book_id)
            member = Member.objects.get(id=member_id)
        except (Book.DoesNotExist, Member.DoesNotExist):
            return Response({'error': 'Invalid book or member ID'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the book is available
        if book.copies_available < 1:
            return Response({'error': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)

        # Reduce the available copies of the book
        book.copies_available -= 1
        book.save()

        # Create the loan
        loan = Loan.objects.create(
            book_id=book,
            member_id=member,
            borrowed_date=now().date(),
            due_date=now().date() + timedelta(days=14)  # Example: 14-day loan period
        )
        serializer = self.get_serializer(loan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# Return a Book
class ReturnBookView(UpdateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request):
        loan_id = request.data.get('id')

        if not loan_id:
            return Response({"error": "Loan ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the loan exists
        try:
            loan = Loan.objects.get(id=loan_id)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update returned_date
        loan.returned_date = now().date()

        # Calculate fine if overdue
        loan.calculate_fine()

        # Increase available copies of the book
        loan.book_id.copies_available += 1
        loan.book_id.save()
        loan.save()

        return Response({"message": "Book returned successfully", "fine": loan.fine})

class LoanListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class LoanDetailView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


