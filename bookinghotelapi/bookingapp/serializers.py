from rest_framework import serializers
from .models import (Employee, Customer, User, Voucher, VoucherRom,
                     HotelRom, TypeRoom, Role, RomImages, Province, Comment,
                     HotelService, Hotel, HotelImages, HotelRequest, Bookings, BookingRoom)


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['avatar'] = instance.avatar.url
        return req


class ImageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['image'] = instance.avatar.url
        return req


class TypeRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeRoom
        fields = '__all__'


class EmployeeSerializer(ItemSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class CustomerSerializer(ItemSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class UserSerializer(ItemSerializer):
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'avatar', 'role', 'is_staff']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class HotelImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImages
        fields = ['id', 'image', 'hotel', 'hotelrequest', 'status']


class HotelRequestSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True, required=False)
    image = serializers.ImageField(required=False)
    status = serializers.ChoiceField(choices=HotelRequest.STATUS_CHOICES, required=False)

    class Meta:
        model = HotelRequest
        fields = ['id', 'user', 'province', 'hotel_name', 'rom_quality', 'hotel_desc', 'hotel_address',
                  'hotel_phone', 'hotel_email', 'image', 'images', 'status']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        hotel_request = HotelRequest.objects.create(**validated_data)

        if images:
            for image in images:
                HotelImages.objects.create(hotelrequest=hotel_request, image=image)

        return hotel_request

    def update(self, instance, validated_data):
        images = validated_data.pop('images', None)
        instance.province = validated_data.get('province', instance.province)
        instance.hotel_name = validated_data.get('hotel_name', instance.hotel_name)
        instance.rom_quality = validated_data.get('rom_quality', instance.rom_quality)
        instance.hotel_desc = validated_data.get('hotel_desc', instance.hotel_desc)
        instance.hotel_address = validated_data.get('hotel_address', instance.hotel_address)
        instance.hotel_phone = validated_data.get('hotel_phone', instance.hotel_phone)
        instance.hotel_email = validated_data.get('hotel_email', instance.hotel_email)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if images is not None:
            HotelImages.objects.filter(hotelrequest=instance).delete()
            for image in images:
                HotelImages.objects.create(hotelrequest=instance, image=image)

        return instance


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'user', 'province', 'hotel_name', 'rom_quality', 'hotel_desc', 'hotel_address',
                  'hotel_phone', 'hotel_email', 'image']


class RomImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RomImages
        fields = ['id', 'image', 'hotel_room']


class HotelRomSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True, required=False)

    class Meta:
        model = HotelRom
        fields = '__all__'

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        hotel_room = HotelRom.objects.create(**validated_data)

        if images:
            for image in images:
                # Đảm bảo sử dụng trường đúng tên
                RomImages.objects.create(hotel_room=hotel_room, image=image)

        return hotel_room


class HotelRomSuaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRom
        fields = [
            'name',
            'bed_quality',
            'price_adult',
            'price_child',
            'price_pet',
            'description',
            'image',
            'total_rooms',
            'additional_child_fee',
            'additional_pet_fee',
            'applies_additional_child_fee',
            'applies_additional_pet_fee',
            'available_rooms',
        ]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'cleanliness_rating',
            'comfort_rating',
            'food_rating',
            'location_rating',
            'service_rating',
            'user',
            'average_rating',
            'created_date',
        ]


class HotelServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelService
        fields = '__all__'


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'


class VoucherRomSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherRom
        fields = '__all__'


class BookingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRoom
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ['id', 'customer', 'hotel_rom', 'check_in_date', 'check_out_date', 'total_amount', 'payment_method',
                  'voucher', 'is_canceled', 'cancelable_until', 'adults', 'children', 'pets', 'hotel', 'created_date', 'is_checked_out']
