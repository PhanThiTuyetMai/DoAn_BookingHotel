from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from cloudinary.models import CloudinaryField
from datetime import timedelta


class BaseModel(models.Model):
    # objects = models.Manager()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True)
    avatar = CloudinaryField(null=True)


class TypeRoom(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Customer(BaseModel):
    name = models.CharField(max_length=255)
    birthday = models.CharField(max_length=255)
    sex = models.CharField(max_length=25)
    address = models.CharField(max_length=255)
    cccd = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    avatar = CloudinaryField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Employee(BaseModel):
    name = models.CharField(max_length=255)
    birthday = models.CharField(max_length=255)
    sex = models.CharField(max_length=25)
    address = models.CharField(max_length=255)
    cccd = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    avatar = CloudinaryField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class HotelRequest(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=255)
    rom_quality = models.CharField(max_length=255)
    hotel_desc = models.TextField()
    hotel_address = models.CharField(max_length=255)
    hotel_phone = models.CharField(max_length=255)
    hotel_email = models.EmailField(max_length=255)
    image = CloudinaryField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Request for {self.hotel_name} by {self.user.username} ({self.status})"


class Hotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    province = models.ForeignKey('Province', on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=255)
    rom_quality = models.CharField(max_length=255)
    hotel_desc = models.TextField()
    hotel_address = models.CharField(max_length=255)
    hotel_phone = models.CharField(max_length=255)
    hotel_email = models.EmailField(max_length=255)
    image = CloudinaryField(null=True, blank=True)

    def __str__(self):
        return self.hotel_name


class HotelImages(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    hotelrequest = models.ForeignKey(HotelRequest, on_delete=models.CASCADE, default=1, null=True)
    image = CloudinaryField(null=True)
    status = models.CharField(max_length=20, default='active')

    def __str__(self):
        return f"Image for hotel {self.hotel.id if self.hotel else 'Request'}"


class RomInteraction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user_id} - {self.hotel_id}'

    class Meta:
        abstract = True


class HotelRom(RomInteraction):
    type = models.ForeignKey(TypeRoom, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    bed_quality = models.CharField(max_length=255)
    price_adult = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_child = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_pet = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=255)
    image = CloudinaryField(null=True)
    total_rooms = models.IntegerField(default=0)
    additional_child_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    additional_pet_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    applies_additional_child_fee = models.BooleanField(default=False)
    applies_additional_pet_fee = models.BooleanField(default=False)
    available_rooms = models.PositiveIntegerField(default=0)


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, default='')

    def __str__(self):
        return f'{self.user_id} - {self.hotel_id}'

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255)
    cleanliness_rating = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    comfort_rating = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    food_rating = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    location_rating = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    service_rating = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)


class RomImages(BaseModel):
    hotel_room = models.ForeignKey(HotelRom, on_delete=models.CASCADE)
    image = CloudinaryField(null=True)


class Voucher(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    discount_percentage = models.CharField(max_length=255)
    discount_amount = models.CharField(max_length=255)
    start_date = models.CharField(max_length=255)
    end_date = models.CharField(max_length=255)
    min_booking_amount = models.CharField(max_length=255)
    max_uses = models.CharField(max_length=255, default=1)
    current_uses = models.CharField(max_length=255, default=0)


class VoucherRom(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    hotel_room = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)


class Bookings(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hotel_rom = models.ForeignKey(HotelRom, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    check_in_date = models.CharField(max_length=255)
    check_out_date = models.CharField(max_length=255)
    total_amount = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255, default="Trực tiếp")
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, null=True, blank=True)
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)
    pets = models.IntegerField(default=0)
    is_checked_out = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    cancelable_until = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.cancelable_until = timezone.now() + timedelta(minutes=1)
        super().save(*args, **kwargs)


class BookingRoom(models.Model):
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE)
    rom = models.ForeignKey(HotelRom, on_delete=models.CASCADE)
    discount_price = models.CharField(max_length=255)


class HotelService(BaseModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    service = models.TextField(max_length=255, default='Không có')
    activity = models.TextField(max_length=255, default='Không có')
    cuisine = models.TextField(max_length=255, default='Không có')
    room_amenity = models.TextField(max_length=255, default='Không có')
    office_amenity = models.TextField(max_length=255, default='Không có')
    nearby_amenity = models.TextField(max_length=255, default='Không có')
    family_friendly_amenity = models.TextField(max_length=255, default='Không có')
    transportation_amenity = models.TextField(max_length=255, default='Không có')
    disability_support_amenity = models.TextField(max_length=255, default='Không có')
    child_friendly_amenity = models.TextField(max_length=255, default='Không có')
    pet_friendly_amenity = models.TextField(max_length=255, default='Không có')
