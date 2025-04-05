from django.db import models
from taggit.managers import TaggableManager
from core.settings import settings


class EventCategories(models.Model):
    categories = models.CharField(max_length=100, unique=True)
    tags = TaggableManager()
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self):
        return f"{self.categories} {self.tags} {self.slug}"


class VenueOfEvent(models.Model):
    place = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200, unique=True)
    capacity = models.IntegerField()
    seating_layout = models.JSONField()
    amenties = models.JSONField()
    other_details = models.JSONField()


class Event(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=100, unique=True, name="name-of-event")
    description = models.TextField()
    category = models.ForeignKey(EventCategories, on_delete=models.PROTECT, related_name="events"
    )
    VenueOfEvent = models.ForeignKey(VenueOfEvent, on_delete=models.PROTECT, related_name="events", name="venue-of-event")
    starting-time = models.DateTimeField()
    ending-time = models.DateTimeField()
    image = models.ImageField(upload_to="events_image/", null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    partnership = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    
    def __str__(self):
        return f"{self.title} {self.description} {self.category} {self.VenueOfEvent} {self.starting-time} {self.ending-time} {self.image} {self.is_featured} {self.created_at} {self.partnership} {self.updated_at} {self.tags}"
    

class TicketType(models.Model):
    TicketTypes = (
    ("VIP", "VIP"),
    ("Regular", "Regular"),
    ("Early Bird", "Early Bird"),
    ("Group", "Group"),
    ("Student", "Student"),
    ("Premium", "Premium")
)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket_types")
    ticket_type = models.CharField(max_length=100, choices=TicketTypes)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.IntegerField()
    sold_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Bookings(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

  
class TicketbookingSys(models.Model):
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    seat_numbers = models.JSONField(default=list, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

