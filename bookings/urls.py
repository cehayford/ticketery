from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (EventCategoriesViewSet, VenueOfEventViewSet, EventViewSet, TicketTypeViewSet, TicketBookingViewSet,)

router = DefaultRouter()
router.register(r'event-categories', EventCategoriesViewSet, basename='event-categories')
router.register(r'venues', VenueOfEventViewSet, basename='venues')
router.register(r'events', EventViewSet, basename='events')
router.register(r'ticket-types', TicketTypeViewSet, basename='ticket-types')
router.register(r'ticket-bookings', TicketBookingViewSet, basename='ticket-bookings')

urlpatterns = [
    path('/bookings/', include(router.urls)),
]