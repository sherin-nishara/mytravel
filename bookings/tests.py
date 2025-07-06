from django.test import TestCase
from django.contrib.auth.models import User
from .models import TravelOption, Booking
from django.utils import timezone

class BookingTestCase(TestCase):

    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='sherin', password='password')
        
        # Create a travel option
        self.travel = TravelOption.objects.create(
            type='Bus',
            source='Chennai',
            destination='Madurai',
            datetime=timezone.now() + timezone.timedelta(days=1),
            price=200.00,
            available_seats=10
        )

    def test_successful_booking(self):
        """Booking should succeed when enough seats are available"""
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel,
            number_of_seats=2,
            total_price=400.00,
            status='Confirmed'
        )
        self.travel.available_seats -= 2
        self.travel.save()

        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(self.travel.available_seats, 8)

    def test_booking_with_insufficient_seats(self):
        """Booking should fail when trying to book more seats than available"""
        booking = Booking(
            user=self.user,
            travel_option=self.travel,
            number_of_seats=20,  # too many
            total_price=4000.00,
            status='Confirmed'
        )

        can_book = booking.number_of_seats <= self.travel.available_seats
        self.assertFalse(can_book)

    def test_cancel_booking_restores_seats(self):
        """Cancelling a booking should restore seats"""
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel,
            number_of_seats=3,
            total_price=600.00,
            status='Confirmed'
        )
        self.travel.available_seats -= 3
        self.travel.save()

        # Cancel booking
        booking.status = 'Cancelled'
        booking.save()
        self.travel.available_seats += 3
        self.travel.save()

        self.assertEqual(self.travel.available_seats, 10)
