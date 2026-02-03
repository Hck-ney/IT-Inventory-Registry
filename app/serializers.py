from rest_framework import serializers
from .models import Asset, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):
    # This makes the employee name visible in the API instead of just an ID
    current_user_name = serializers.ReadOnlyField()

    class Meta:
        model = Asset
        fields = ['Asset_ID', 'name', 'category', 'status', 'assigned_to', 'current_user_name']