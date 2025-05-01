from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class EventCategoriesSerializer(ModelSerializer):
    class Meta:
        model = EventCategories
        fields = ["categories", "tags"]
        extra_kwargs = {
            "categories": {"error_messages": {"blank": _("This field for categories may not be blank.")}},
            "tags": {"error_messages": {"blank": _("This field for tags may not be blank.")}},
        }

        def get_tags(self, obj):
            return [tag.name for tag in obj.tags.all()]


class VenueOfEventSerializer(ModelSerializer):
    class Meta:
        model = VenueOfEvent
        fields = "__all__"


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields  = ['id', 'title', 'description', 'category', 'VenueOfEvent', 'starting_time', 'ending_time', 'image', 'is_featured', 'created_at', 'partnership', 'updated_at', 'tags']
        
        def get_tags(self, obj):
            return [tag.name for tag in obj.tags.all()]


class TicketTypeSerializer(ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['event', 'ticket_type', 'price', 'quantity_available', 'sold_quantity', 'created_at']


# booking serializer
class BookingsSerializer(ModelSerializer):
    class Meta:
        model = Bookings
        fields = "__all__"


class TicketBookingSysSerializer(ModelSerializer):
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = TicketBookingSys
        fields = ["id", "booking", "ticket_type", "quantity", "seat_numbers", "unit_price", "total_price"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["ticket_type_details"] = {
            "type": instance.ticket_type.ticket_type,
            "price": instance.ticket_type.price,
        }
        return representation
