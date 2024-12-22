from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    copies_available = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title
    
class Member(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    
class Loan(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    fine = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def calculate_fine(self):
        """
        Calculate the fine for overdue books.
        Assume a fine rate of 10 per day.
        """
        if self.returned_date and self.returned_date > self.due_date:
            overdue_days = (self.returned_date - self.due_date).days
            self.fine = overdue_days * 10.0  # Fine rate is 10 per day
            self.save()
        return self.fine

    def __str__(self):
        return f"Loan: {self.book.title} to {self.member.name}"
