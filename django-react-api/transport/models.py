from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class Transport(models.Model):
    BUS = "Bus"
    CAR = "Car pooling"

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
    transport_type = models.CharField(choices=TRANSPORT_CHOICES, max_length=25, default=BUS)
    vehicle_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)
    vehicle_seats_plan = models.FileField(null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    available_days = ArrayField(
        models.CharField(choices=WorkingDays),
        default=["Mon", "Tue", "Wed", "Thurs", "Fri", "Sat", "Sun"]
    )


class BookingInformation(models.Model):
    MALE = "M"
    FEMALE = "F"

    GENDER_CHOICES = (
        (MALE, "M"),
        (FEMALE, "F")
    )
    from_location = models.CharField(max_length=50)
    to_location = models.CharField(max_length=50)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    seat_number = models.CharField(null=True, blank=True)
