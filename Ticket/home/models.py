# models.py
from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    seat_limit = models.PositiveIntegerField()
    booked_seats = models.PositiveIntegerField(default=0)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title


class Ticket(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    event       = models.ForeignKey(Event, on_delete=models.CASCADE)
    # ― student‑specific fields ―
    student_name = models.CharField(max_length=120)
    branch       = models.CharField(max_length=120)
    year         = models.CharField(max_length=10)
    email        = models.EmailField()
    mobile       = models.CharField(max_length=15)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    booked_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} — {self.event.title}"


class Review(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.rating}★)"
