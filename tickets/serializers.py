from rest_framework import serializers
from tickets.models import *


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        # serialize data by wrong way the right ways is (uuid, slug)
        fields = ["pk", "reservation", "name", "mobile", "email"]
