from MyRelevate import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined',
                  'confirmed','is_contributor','contributo_profile','objects')
