from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

from movierater.mixin import UUIDMixin

# Create your models here.


class Route(UUIDMixin):
    from_location = models.CharField(max_length=50)
    to_location = models.CharField(max_length=50)
    route_name = models.CharField(max_length=150, editable=False)


class Transport(UUIDMixin):
    BUS = "Bus"
    CAR = "Car pooling"

    SLEEPER = "SL"
    SEATER = "SR"

    BUS_TYPES = (
        (SLEEPER, "Sleeper"),
        (SEATER, "Seater")
    )
    # working days
    MONDAY = "Mon"
    TUESDAY = "Tue"
    WEDNESDAY = "Wed"
    THURSDAY = "Thurs"
    FRIDAY = "Fri"
    SATURDAY = "Sat"
    SUNDAY = "Sun"

    WorkingDays = (
        (MONDAY, "MONDAY"),
        (TUESDAY, "TUESDAY"),
        (WEDNESDAY, "WEDNESDAY"),
        (THURSDAY, "THURSDAY"),
        (FRIDAY, "FRIDAY"),
        (SATURDAY, "SATURDAY"),
        (SUNDAY, "SUNDAY"),

    )
    TRANSPORT_CHOICES = (
        (BUS, "Travel Bus"),
        (CAR, "Car"),
    )
    SEATING_PATTERNS =(
        ("BUS_1", "2+2 seater"),
        ("BUS_2", "2+1 seater"),
        ("BUS_3", "2+1 sleeper")
    )
    transport_type = models.CharField(choices=TRANSPORT_CHOICES, max_length=25, default=BUS)
    vehicle_number = models.CharField(max_length=10, unique=True)
    is_available = models.BooleanField(default=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    bus_type = models.CharField(max_length=2, choices=BUS_TYPES)
    seat_pattern = models.CharField(max_length=50, choices=SEATING_PATTERNS)
    capacity = models.IntegerField(default=0)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="buses")


class Seat(UUIDMixin):
    number = models.CharField(max_length=4)
    price = models.PositiveIntegerField(default=0)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name="seats")
    status = models.CharField(
        max_length=20,
        choices=(
            ('Available', 'available'),
            ('Reserved', 'reserved'),
        ),
        default='Available'
    )


class Booking(UUIDMixin):
    MALE = "M"
    FEMALE = "F"

    GENDER_CHOICES = (
        (MALE, "M"),
        (FEMALE, "F")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    gender = models.CharField(choices=GENDER_CHOICES, max_length=2)
    age = models.PositiveIntegerField()
    seat_number = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="booked_users")
    payment_mode = models.CharField(max_length=25)
    email = models.EmailField()
    phone_number = models.IntegerField()


class Wallet(UUIDMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
