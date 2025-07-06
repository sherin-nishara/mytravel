from django.db import models
from django.contrib.auth.models import User

class TravelOption(models.Model):
    TRAVEL_TYPE = [('Flight', 'Flight'), ('Train', 'Train'), ('Bus', 'Bus')]
    type = models.CharField(max_length=10, choices=TRAVEL_TYPE)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField()

class Booking(models.Model):
    STATUS = [('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)
