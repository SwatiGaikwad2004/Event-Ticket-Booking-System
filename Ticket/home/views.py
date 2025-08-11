from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import send_mail
from .forms import TicketForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from .models import Event, Ticket, Review
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import ProfileEditForm
from .forms import EventForm 

from django.db.models import Q
from .forms import ReviewForm







# ---------------- Home ----------------
def home(request):
    events = Event.objects.filter(date__gte=timezone.now())
    return render(request, 'home.html', {'events': events})


# ---------------- Auth ----------------

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name'] 
        last_name = request.POST['last_name']    

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Please enter both username and password")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# ---------------- Event detail ----------------


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    bookings = Ticket.objects.filter(event=event)
    available_seats = event.seat_limit - bookings.count()

    user_has_booked = False
    if request.user.is_authenticated:
        user_has_booked = bookings.filter(user=request.user).exists()

    # Handle review form
    if request.method == 'POST' and user_has_booked:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.event = event
            review.save()
            messages.success(request, "Review submitted successfully!")
            return redirect('event_detail', event_id=event.id)
    else:
        form = ReviewForm()

    reviews = Review.objects.filter(event=event)

    return render(request, 'event_detail.html', {
        'event': event,
        'available_seats': available_seats,
        'user_has_booked': user_has_booked,
        'form': form,
        'reviews': reviews,
    })

def book_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ticket = Ticket.objects.create(
                user=request.user,
                event=event,
                student_name=data['student_name'],
                branch=data['branch'],
                year=data['year'],
                email=data['email'],
                mobile=data['mobile'],
                paid_amount=data.get('paid_amount', 0)
            )

            # Send confirmation email
            send_mail(
                subject='🎟️ Ticket Booked Successfully!',
                message=f"Hello {ticket.student_name},\nYour ticket for '{event.title}' has been booked successfully.\nAmount Paid: ₹{ticket.paid_amount}",
                from_email='swatirgaikwad1436@gmail.com',
                recipient_list=[ticket.email],
                fail_silently=False,
            )

            messages.success(request, "Payment successful. Ticket booked!")
            return redirect('home')  
    else:
        form = TicketForm()

    return render(request, 'book_ticket_form.html', {'form': form, 'event': event})

# ---------------- My bookings ----------------
@login_required
def my_bookings(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'tickets': tickets})
#-------------------------------------------------



@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, "Profile updated successfully.")
        
       
        return redirect('home') 
    
    return render(request, 'edit_profile.html')



#--------------------------------------------



def dummy_payment(request):
    booking_data = request.session.get('booking_data')
    event_id = request.session.get('event_id')
    event = get_object_or_404(Event, id=event_id)

    if not booking_data:
        return redirect('home')

    if request.method == 'POST':
       
        ticket = Ticket.objects.create(
            user=request.user,
            event=event,
            student_name=booking_data['student_name'],
            branch=booking_data['branch'],
            year=booking_data['year'],
            email=booking_data['email'],
            mobile=booking_data['mobile'],
            paid_amount=0 
        )
        
        send_mail(
            'Ticket Booked Successfully!',
            f'Hi {ticket.student_name}, your ticket for {event.title} is booked.',
            'your_email@gmail.com',
            [ticket.email],
            fail_silently=True,
        )

        messages.success(request, 'Payment successful. Ticket booked!')
        return redirect('my_bookings')

    return render(request, 'dummy_payment.html', {'event': event})


#-----------------------------------------------------------------

@login_required
def host_dashboard(request):
    user_events = Event.objects.filter(created_by=request.user)
    return render(request, 'host_dashboard.html', {'events': user_events})

@login_required
def view_bookings(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    tickets = Ticket.objects.filter(event=event)
    return render(request, 'view_bookings.html', {'event': event, 'tickets': tickets})



def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('host_dashboard')
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'form': form})

#----------------------------------------------------------


def home(request):
    query = request.GET.get('q')
    if query:
        events = Event.objects.filter(title__icontains=query)
    else:
        events = Event.objects.all()
    return render(request, 'home.html', {'events': events})
 
@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user   
            event.save()
            messages.success(request, ' Event created successfully!')
            return redirect('host_dashboard')  
        else:
            print(form.errors) 
            messages.error(request, ' Form is invalid. Please check your inputs.')
    else:
        form = EventForm()
    return render(request, 'event.html', {'form': form})



@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('host_dashboard')

    return redirect('host_dashboard')