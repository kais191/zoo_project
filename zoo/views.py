from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from .forms import BookingForm
from .models import Booking
from blog.forms import BlogPostForm  # Import BlogPostForm for add_post
import datetime
import requests


def home(request):
    return render(request, "zoo/home.html")


@login_required
def book_ticket(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('profile')
    else:
        form = BookingForm()
    return render(request, "zoo/book_ticket.html", {'form': form})


@login_required
def profile(request):
    past_bookings = Booking.objects.filter(
        user=request.user, date__lt=datetime.date.today()
    ).order_by("-date")
    upcoming_bookings = Booking.objects.filter(
        user=request.user, date__gte=datetime.date.today()
    ).order_by("date")

    # Fetch weather data
    city = request.GET.get("city", "London")  # Default city is London
    weather_data = []
    if city:
        api_key = "c766af7adf104f57db1f29c570ea1a05"  # Replace with your API key
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            forecast = response.json().get("list", [])[:7]  # Get 7 days of data
            for item in forecast:
                weather_data.append({
                    "date": item["dt_txt"].split(" ")[0],
                    "temp": item["main"]["temp"],
                    "description": item["weather"][0]["description"].title(),
                })

    return render(request, "zoo/profile.html", {
        "past_bookings": past_bookings,
        "upcoming_bookings": upcoming_bookings,
        "weather_data": weather_data,
        "city": city,
    })


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def add_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Associate the post with the logged-in user
            post.save()
            return redirect('home')  # Redirect to home or another desired page
    else:
        form = BlogPostForm()
    return render(request, "blog/add_post.html", {'form': form})
