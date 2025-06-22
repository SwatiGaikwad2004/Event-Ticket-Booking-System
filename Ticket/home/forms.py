from django import forms
from django.contrib.auth.models import User
from .models import Event
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i}★") for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date', 'seat_limit', 'fee']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class TicketForm(forms.Form):
    student_name = forms.CharField()
    branch = forms.CharField()
    year = forms.CharField()
    email = forms.EmailField()
    mobile = forms.CharField()
    paid_amount = forms.DecimalField(required=False, initial=0)
