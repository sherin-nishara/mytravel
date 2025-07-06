from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileUpdateForm
from .models import TravelOption, Booking
from .forms import BookingForm
from django.utils import timezone
from django.db.models import Q


def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

def travel_list(request):
    travels = TravelOption.objects.all()

    travel_type = request.GET.get('type')
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    
    if travel_type:
        travels = travels.filter(type=travel_type)
    if source:
        travels = travels.filter(source__icontains=source)
    if destination:
        travels = travels.filter(destination__icontains=destination)

    return render(request, 'travel_list.html', {'travels': travels})

@login_required
def book_travel(request, travel_id):
    travel = TravelOption.objects.get(id=travel_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, travel_option=travel)
        if form.is_valid():
            seats = form.cleaned_data['number_of_seats']
            if seats <= 0:
                form.add_error('number_of_seats', 'Enter a valid number of seats.')
            elif seats > travel.available_seats:
                form.add_error('number_of_seats', 'Not enough seats available.')
            else:
                total_price = seats * travel.price
                booking = form.save(commit=False)
                booking.user = request.user
                booking.travel_option = travel
                booking.total_price = total_price
                booking.status = 'Confirmed'
                booking.save()
                travel.available_seats -= seats
                travel.save()
                return render(request, 'booking_success.html', {'booking': booking})
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form, 'travel': travel})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id, user=request.user)
    
    if booking.status == 'Confirmed':
        booking.status = 'Cancelled'
        booking.save()
        
        travel = booking.travel_option
        travel.available_seats += booking.number_of_seats
        travel.save()
        
    return redirect('my_bookings')

def travel_list(request):
    travels = TravelOption.objects.all()

    travel_type = request.GET.get('type')
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    search = request.GET.get('search')

    if travel_type:
        travels = travels.filter(type=travel_type)
    if source:
        travels = travels.filter(source__icontains=source)
    if destination:
        travels = travels.filter(destination__icontains=destination)
    if search:
        travels = travels.filter(
            Q(source__icontains=search) |
            Q(destination__icontains=search)
        )

    return render(request, 'travel_list.html', {'travels': travels})
