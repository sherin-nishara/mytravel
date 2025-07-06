from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    #booking
    path('travels/', views.travel_list, name='travel_list'),
    path('book/<int:travel_id>/', views.book_travel, name='book_travel'),

    #status
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
