from rest_framework import serializers

from .models import (
    Customer,
    HouseOwner,
    HouseImage,
    House,
    Donate,
)


class DonateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Donate
		fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = '__all__'

class HouseOwnerSerializer(serializers.ModelSerializer):
	class Meta:
		model = HouseOwner
		fields = '__all__'


class HouseImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = HouseImage
		fields = '__all__'

class HouseSerializer(serializers.ModelSerializer):
	class Meta:
		model = House
		fields = '__all__'
		depth = 1







