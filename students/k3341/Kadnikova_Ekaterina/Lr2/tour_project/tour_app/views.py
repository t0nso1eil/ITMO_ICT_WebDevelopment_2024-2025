from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .forms import UserRegistrationForm, BookingForm, ReviewForm, TourFilterForm
from .models import Tour, Booking
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('tour_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tour_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def tour_list(request):
    tours = Tour.objects.all()
    form = TourFilterForm(request.GET)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        if name:
            tours = tours.filter(name__icontains=name)
        if start_date:
            tours = tours.filter(start_date__gte=start_date)
        if end_date:
            tours = tours.filter(end_date__lte=end_date)
    context = {
        'tours': tours,
        'form': form
    }
    return render(request, 'tour_list.html', context)

@login_required
def add_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    booking = Booking.objects.filter(user=request.user, tour=tour, is_confirmed=True).first()
    if not booking:
        messages.error(request, "You can't add a review, your booking is not confirmed.")
        return redirect('tour_detail', tour_id=tour_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = tour
            review.save()
            messages.success(request, "Thank you for your review.!")
            return redirect('tour_detail', tour_id=tour_id)
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form, 'tour': tour})

def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    booking = Booking.objects.filter(user=request.user, tour=tour, is_confirmed=True).first()
    reviews = tour.reviews.all()
    context = {
        'tour': tour,
        'agency': tour.agency,
        'reviews': reviews,
        'average_rating': tour.average_rating if tour.average_rating is not None else "No reviews yet",
        'booking_confirmed': booking is not None,
    }
    return render(request, 'tour_detail.html', context)

@login_required
def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if tour.available_seats <= 0:
        messages.error(request, "No available seats for this tour.")
        return redirect('tour_detail', tour_id=tour_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.tour = tour
            booking.save()
            return redirect('tour_list')
    else:
        form = BookingForm()
    return render(request, 'book_tour.html', {'form': form, 'tour': tour})

@login_required
def add_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = tour
            review.save()
            return redirect('tour_detail', tour_id=tour_id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'tour': tour})

def custom_logout(request):
    logout(request)
    return redirect('tour_list')


@permission_required('tour_app.can_confirm_booking', raise_exception=True)
def manage_bookings(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        is_confirmed = request.POST.get('is_confirmed') == 'on'
        booking = Booking.objects.get(id=booking_id)
        booking.is_confirmed = is_confirmed
        booking.save()
        return redirect(reverse('manage_bookings', args=[tour_id]))
    bookings = Booking.objects.filter(tour=tour).select_related('user')
    return render(request, 'booking_management.html', {'bookings': bookings, 'tour': tour})