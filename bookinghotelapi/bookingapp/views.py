from django.shortcuts import render
from rest_framework import viewsets, generics, status, parsers, permissions
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (Employee, Customer, Hotel, HotelImages, HotelRequest, Role, HotelRom, RomImages, Province, User,
                     Comment, HotelService, TypeRoom, VoucherRom, Voucher, BookingRoom, Bookings)
from . import serializers, paginators, prems
from .utils import send_registration_email, send_email_to_user
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from . import prems
import hashlib
from django.http import JsonResponse, HttpRequest
import json
import requests
import hmac
import random
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import urllib.parse
import time
from datetime import datetime


class TypeRoomViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = TypeRoom.objects.filter()
    serializer_class = serializers.TypeRoomSerializer


class EmployeeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Employee.objects.filter(active=True)
    serializer_class = serializers.EmployeeSerializer
    pagination_class = paginators.PagePaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        ma = self.request.query_params.get('ma')
        name = self.request.query_params.get('name')
        print(self.request.user.role)
        print(type(self.request.user.role))
        if self.request.user.role.name != 'quản trị':
            return queryset.none()
        if ma:
            queryset = queryset.filter(id=ma)
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @action(methods=['post'], url_path='them_nv', detail=False)
    def them_nv(self, request):
        if request.user.role.name != 'quản trị':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)
        nhanvien = serializers.EmployeeSerializer(data=request.data)
        if nhanvien.is_valid():
            nhanvien.save()
            return Response(nhanvien.data, status=status.HTTP_201_CREATED)
        return Response(nhanvien.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], url_path='sua_nv', detail=True)
    def sua_nv(self, request, pk):
        if request.user.role.name != 'quản trị':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)
        try:
            nhanvien = Employee.objects.get(id=pk)
        except Employee.DoesNotExist:
            return Response({'message': 'Không tìm thấy nhân viên'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.EmployeeSerializer(nhanvien, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], url_path='xoa_nv', detail=True)
    def xoa_nv(self, request, pk):
        if request.user.role.name != 'quản trị':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)
        nhanvien = Employee.objects.get(id=pk)
        if nhanvien:
            nhanvien.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Customer.objects.filter(active=True)
    serializer_class = serializers.CustomerSerializer
    pagination_class = paginators.PagePaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        ma = self.request.query_params.get('ma')
        name = self.request.query_params.get('name')
        if ma:
            queryset = queryset.filter(id=ma)
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @action(methods=['post'], url_path='them_kh', detail=False)
    def them_kh(self, request):
        khachhang = serializers.CustomerSerializer(data=request.data)
        if khachhang.is_valid():
            khachhang.save()
            return Response(khachhang.data, status=status.HTTP_201_CREATED)
        return Response(khachhang.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], url_path='sua_kh', detail=True)
    def sua_kh(self, request, pk):
        try:
            khachhang = Customer.objects.get(id=pk)
        except Customer.DoesNotExist:
            return Response({'message': 'Không tìm thấy khách hàng'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CustomerSerializer(khachhang, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], url_path='xoa_kh', detail=True)
    def xoa_kh(self, request, pk):
        if self.request.user.role.name != 'quản trị' and self.request.user.role.name != 'nhân viên':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)

        khachhang = Customer.objects.get(id=pk)
        if khachhang:
            khachhang.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RoleViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = serializers.RoleSerializer

    def get_queryset(self):
        queryset = self.queryset
        return queryset

    @action(methods=['post'], url_path='themvitri', detail=False)
    def them_vitri(self, request):
        vitri = serializers.RoleSerializer(data=request.data)
        if vitri.is_valid():
            vitri.save()
            return Response(vitri.data, status=status.HTTP_201_CREATED)
        return Response(vitri.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], url_path='suavitri', detail=True)
    def sua_role(self, request, pk):
        try:
            vitri = Role.objects.get(id=pk)
        except Role.DoesNotExist:
            return Response({'message': 'Không tìm thấy chức vụ'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.RoleSerializer(vitri, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], url_path='xoavitri', detail=True)
    def xoa_vitri(self, request, pk):
        vitri = Role.objects.get(id=pk)
        if vitri:
            vitri.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProvinceViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Province.objects.all()
    serializer_class = serializers.ProvinceSerializer

    def get_queryset(self):
        queryset = self.queryset
        return queryset

    @action(methods=['post'], url_path='them_tinh', detail=False)
    def them_tinh(self, request):
        tinh = serializers.ProvinceSerializer(data=request.data)
        if tinh.is_valid():
            tinh.save()
            return Response(tinh.data, status=status.HTTP_201_CREATED)
        return Response(tinh.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], url_path='sua_tinh', detail=True)
    def sua_tinh(self, request, pk):
        try:
            tinh = Province.objects.get(id=pk)
        except Province.DoesNotExist:
            return Response({'message': 'Không tìm thấy khách sạn'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.ProvinceSerializer(tinh, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], url_path='xoa_tinh', detail=True)
    def xoa_tinh(self, request, pk):
        tinh = Province.objects.get(id=pk)
        if tinh:
            tinh.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class HotelRequestViewSet(viewsets.ModelViewSet):
    queryset = HotelRequest.objects.all()
    serializer_class = serializers.HotelRequestSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], url_path='add_request', detail=False)
    def request_hotel(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Bạn cần đăng nhập để thực hiện hành động này."},
                            status=status.HTTP_401_UNAUTHORIZED)

        if request.user.role.name == 'chủ khách sạn':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)

        user = request.user
        if HotelRequest.objects.filter(user=user, status=HotelRequest.PENDING).exists():
            return Response({"detail": "Bạn đã có một yêu cầu đang chờ xét duyệt."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            hotel_request = serializer.save(user=user)
            images = request.FILES.getlist('images')
            if images:
                for image in images:
                    HotelImages.objects.create(hotelrequest=hotel_request, image=image)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['patch'], url_path='update_status', detail=True)
    def update_status(self, request, pk=None):
        if self.request.user.role.name != 'quản trị' and self.request.user.role.name != 'nhân viên':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)

        try:
            hotel_request = HotelRequest.objects.get(pk=pk)
        except HotelRequest.DoesNotExist:
            return Response({'detail': 'Yêu cầu không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(hotel_request, data=request.data, partial=True)
        if serializer.is_valid():
            status_value = serializer.validated_data.get('status')
            if status_value == HotelRequest.APPROVED:
                # Tạo khách sạn mới từ yêu cầu
                hotel = Hotel.objects.create(
                    user=hotel_request.user,
                    province=hotel_request.province,
                    hotel_name=hotel_request.hotel_name,
                    rom_quality=hotel_request.rom_quality,
                    hotel_desc=hotel_request.hotel_desc,
                    hotel_address=hotel_request.hotel_address,
                    hotel_phone=hotel_request.hotel_phone,
                    hotel_email=hotel_request.hotel_email,
                    image=hotel_request.image
                )

                # Chuyển ảnh từ yêu cầu sang khách sạn
                hotel_images = HotelImages.objects.filter(hotelrequest=hotel_request)
                for img in hotel_images:
                    img.hotel = hotel
                    img.hotelrequest = None
                    img.save()

                hotel_request.delete()

                # Gửi email thông báo
                send_email_to_user(hotel_request.user, hotel_request)

            serializer.save()  # Cập nhật trạng thái yêu cầu
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HotelViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = serializers.HotelSerializer
    pagination_class = paginators.PagePaginator

    def get_queryset(self):
        queryset = self.queryset
        ma = self.request.query_params.get('ma')
        name = self.request.query_params.get('name')
        user_id = self.request.query_params.get('user_id')
        if ma:
            queryset = queryset.filter(id=ma)
        if name:
            queryset = queryset.filter(hotel_name__icontains=name)
        if user_id:
            queryset = queryset.filter(user=user_id)

        return queryset

    def search_hotels(self, request):
        province_id = request.query_params.get('province')
        check_in_date = request.query_params.get('check_in')
        check_out_date = request.query_params.get('check_out')
        adults = int(request.query_params.get('adults', 1))
        children = int(request.query_params.get('children', 0))
        pets = int(request.query_params.get('pets', 0))

        hotels = Hotel.objects.filter(province_id=province_id)
        available_hotels = []

        if check_in_date and check_out_date:
            for hotel in hotels:
                # Lọc các phòng có sẵn
                rooms = HotelRom.objects.filter(hotel=hotel, available_rooms__gt=0)

                # Kiểm tra xem có phòng nào phù hợp với số lượng người
                for room in rooms:
                    if (adults + children) <= room.total_rooms:
                        total_price = (adults * room.price_adult) + \
                                      (children * room.price_child) + \
                                      (pets * room.price_pet)

                        # Nếu có ít nhất một phòng phù hợp, thêm khách sạn vào danh sách
                        available_hotels.append({
                            'id': hotel.id,
                            'hotel_name': hotel.hotel_name,
                            'hotel_address': hotel.hotel_address,
                            'image': hotel.image.url,
                            'rom_quality': hotel.rom_quality
                        })
                        break  # Không cần kiểm tra thêm phòng nếu đã tìm thấy một phòng hợp lệ

        # Trả về danh sách khách sạn có sẵn
        return Response({'available_hotels': available_hotels})

    @action(methods=['post'], url_path='them_khachsan', detail=False)
    def them_hotel(self, request):
        if self.request.user.role.name != 'quản trị' and self.request.user.role.name != 'nhân viên':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)

        hotel = serializers.HotelSerializer(data=request.data)
        if hotel.is_valid():
            hotel.save()
            return Response(hotel.data, status=status.HTTP_201_CREATED)
        return Response(hotel.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['patch'], url_path='sua_khachsan', detail=True)
    def sua_hotel(self, request, pk):
        if self.request.user.role.name != 'chủ khách sạn':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)

        try:
            hotel = Hotel.objects.get(id=pk)
        except Hotel.DoesNotExist:
            return Response({'message': 'Không tìm thấy khách sạn'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.HotelSerializer(hotel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], url_path='xoa_khachsan', detail=True)
    def xoa_hotel(self, request, pk):
        if self.request.user.role.name != 'quản trị' and self.request.user.role.name != 'nhân viên':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)

        hotel = Hotel.objects.get(id=pk)
        if hotel:
            hotel.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.select_related('user').order_by('-id')
        paginator = paginators.PagePaginator()
        page = paginator.paginate_queryset(comments, request)
        if page is not None:
            serializer = serializers.CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        return Response(serializers.CommentSerializer(comments, many=True).data)

    @action(methods=['post'], url_path='them_comments', detail=True)
    def add_comment(self, request, pk):
        hotel = self.get_object()
        content = request.data.get('content')
        cleanliness_rating = request.data.get('cleanliness_rating')
        comfort_rating = request.data.get('comfort_rating')
        food_rating = request.data.get('food_rating')
        location_rating = request.data.get('location_rating')
        service_rating = request.data.get('service_rating')
        average_rating = request.data.get('average_rating')

        if not content:
            return Response({"error": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)

        comment = hotel.comment_set.create(
            content=content,
            cleanliness_rating=cleanliness_rating,
            comfort_rating=comfort_rating,
            food_rating=food_rating,
            location_rating=location_rating,
            service_rating=service_rating,
            user=request.user,
            average_rating=average_rating,
        )
        return Response(serializers.CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


class HotelImagesViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = HotelImages.objects.all()
    serializer_class = serializers.HotelImagesSerializer

    def get_queryset(self):
        queryset = self.queryset
        mahotel = self.request.query_params.get('mahotel')
        if mahotel:
            queryset = queryset.filter(hotel=mahotel)
        return queryset

    @action(methods=['patch'], url_path='sua_anhhotel', detail=True)
    def sua_anhhotel(self, request, pk):
        try:
            anh = HotelImages.objects.get(id=pk)
        except HotelImages.DoesNotExist:
            return Response({'message': 'Không tìm thấy ảnh'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.HotelImagesSerializer(anh, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HotelRoomViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = HotelRom.objects.all()
    serializer_class = serializers.HotelRomSerializer
    pagination_class = paginators.RoomPagePaginator

    def get_queryset(self):
        queryset = self.queryset
        mahotel = self.request.query_params.get('mahotel')
        ma = self.request.query_params.get('ma')
        if mahotel:
            queryset = queryset.filter(hotel=mahotel)
        if ma:
            queryset = queryset.filter(id=ma)

        return queryset

    @action(methods=['post'], url_path='them_phong', detail=False)
    def them_hotelroom(self, request):
        if self.request.user.role.name != 'chủ khách sạn':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)
        user = request.user
        if user.is_authenticated:
            serializer = self.get_serializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                hotel_room = serializer.save(user=user)
                print(hotel_room)

                images = request.FILES.getlist('images')
                if images:
                    for image in images:
                        RomImages.objects.create(hotel_room=hotel_room, image=image)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Not authenticated"},
                        status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['patch'], url_path='sua_phong', detail=True)
    def sua_phong(self, request, pk):
        if self.request.user.role.name != 'chủ khách sạn':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)
        try:
            phong = HotelRom.objects.get(id=pk)
        except HotelRom.DoesNotExist:
            return Response({'message': 'Không tìm thấy  phòng'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.HotelRomSuaSerializer(phong, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], url_path='xoa_phong', detail=True)
    def xoa_hotelroom(self, request, pk):
        if self.request.user.role.name != 'chủ khách sạn':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)
        hotelroom = HotelRom.objects.get(id=pk)
        if hotelroom:
            hotelroom.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], url_path='gia_phong_re_nhat', detail=False)
    def gia_phong_re_nhat(self, request):
        mahotel = request.query_params.get('mahotel')
        if not mahotel:
            return Response({'error': 'Thiếu tham số mahotel.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rooms = HotelRom.objects.filter(hotel=mahotel)
            if not rooms.exists():
                return Response({'error': 'Không tìm thấy phòng cho khách sạn này.'}, status=status.HTTP_404_NOT_FOUND)

            # Tìm giá phòng thấp nhất
            lowest_price_room = min(rooms, key=lambda room: room.price_adult)
            serializer = self.get_serializer(lowest_price_room)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], url_path='confirm-checkout', detail=True)
    def confirm_checkout(self, request, pk=None):
        if self.request.user.role.name != 'chủ khách sạn':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)

        room = HotelRom.objects.get(id=pk)

        bookings = Bookings.objects.filter(hotel_rom=room)
        for booking in bookings:
            booking.is_checked_out = True
            booking.save()

        room.available_rooms += 1
        room.save()

        return Response({'success': True, 'available_rooms': room.available_rooms}, status=status.HTTP_200_OK)


class RomImagesViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = RomImages.objects.all()
    serializer_class = serializers.RomImagesSerializer

    def get_queryset(self):
        queryset = self.queryset
        maroom= self.request.query_params.get('maroom')
        if maroom:
            queryset = queryset.filter(hotel_room=maroom)
        return queryset

    @action(methods=['post'], url_path='them_anhphong', detail=False)
    def them_anhphong(self, request):
        anh = serializers.RomImagesSerializer(data=request.data)
        if anh.is_valid():
            anh.save()
            return Response(anh.data, status=status.HTTP_201_CREATED)
        return Response(anh.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], url_path='sua_anhphong', detail=True)
    def sua_anhphong(self, request, pk):
        try:
            anh = RomImages.objects.get(id=pk)
        except RomImages.DoesNotExist:
            return Response({'message': 'Không tìm thấy ảnh'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.RomImagesSerializer(anh, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], url_path='xoa_anhphong', detail=True)
    def xoa_anhphong(self, request, pk):
        anh = RomImages.objects.get(id=pk)
        if anh:
            anh.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='list_user', detail=False)
    def list_users(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get', 'patch'], url_path='current_user', detail=False)
    def current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(serializers.UserSerializer(user).data)

    @action(methods=['post'], url_path='register', detail=False)
    def register_user(self, request):
        print("Register user method called")
        if request.method == 'POST':
            serializer = serializers.UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                print("User email:", user.email)  # Debugging statement
                send_registration_email(user.email)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = prems.CommentOwner


class HotelServiceViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = HotelService.objects.all()
    serializer_class = serializers.HotelServiceSerializer

    def get_queryset(self):
        queryset = self.queryset
        maht = self.request.query_params.get('maht')
        if maht:
            queryset = queryset.filter(hotel=maht)
        return queryset

    @action(methods=['post'], url_path='them_dichvu', detail=False)
    def them_dichvu(self, request):
        if self.request.user.role.name != 'chủ khách sạn':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)
        hotelservice = serializers.HotelServiceSerializer(data=request.data)
        if hotelservice.is_valid():
            hotelservice.save()
            return Response(hotelservice.data, status=status.HTTP_201_CREATED)
        return Response(hotelservice.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], url_path='sua_dichvu', detail=True)
    def sua_dichvu(self, request, pk):
        if self.request.user.role.name != 'chủ khách sạn':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)
        try:
            hotelservice = HotelService.objects.get(id=pk)
        except HotelService.DoesNotExist:
            return Response({'message': 'Không tìm thấy chức vụ'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.HotelServiceSerializer(hotelservice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], url_path='xoa_dichvu', detail=True)
    def xoa_dichvu(self, request, pk):
        if self.request.user.role.name != 'chủ khách sạn':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)
        hotelservice = HotelService.objects.get(id=pk)
        if hotelservice:
            hotelservice.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class VoucherViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Voucher.objects.all()
    serializer_class = serializers.VoucherSerializer

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user=user)
        return queryset

    @action(methods=['get'], url_path='hethan_voucher', detail=False)
    def check_expired(self, request):
        now = timezone.now()
        expired_vouchers = Voucher.objects.filter(end_date__lt=now)
        expired_vouchers.delete()
        return Response(self.get_queryset().values())

    @action(methods=['post'], url_path='add_voucher', detail=False)
    def create_voucher(self, request):
        if self.request.user.role.name == 'người dùng':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)

        voucher_data = request.data.get('voucher')
        hotel_id = request.data.get('hotel')

        voucher_serializer = serializers.VoucherSerializer(data=voucher_data)
        if voucher_serializer.is_valid():
            voucher = voucher_serializer.save()
            if hotel_id:
                try:
                    hotel = Hotel.objects.get(id=hotel_id)
                    VoucherRom.objects.create(voucher=voucher, hotel_room=hotel)
                except Hotel.DoesNotExist:
                    return Response({'error': 'Khách sạn không tồn tại.'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(voucher_serializer.data, status=status.HTTP_201_CREATED)

        return Response(voucher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], url_path='sua_voucher', detail=False)
    def update_voucher(self, request, pk=None):
        if self.request.user.role.name == 'người dùng':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)
        try:
            voucher = Voucher.objects.get(pk=pk)
        except Voucher.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        voucher_data = request.data.get('voucher')
        room_ids = request.data.get('rooms', [])

        for attr, value in voucher_data.items():
            setattr(voucher, attr, value)
        voucher.save()

        # Xóa các liên kết cũ và thêm mới
        VoucherRom.objects.filter(voucher=voucher).delete()
        for room_id in room_ids:
            VoucherRom.objects.create(voucher=voucher, hotel_room_id=room_id)

        return Response(serializers.VoucherSerializer(voucher).data)

    @action(methods=['delete'], url_path='xoa_voucher', detail=True)
    def xoa_voucher(self, request, pk):
        if self.request.user.role.name == 'người dùng':
            return Response({'message': 'Không đủ quyền truy cập'}, status=status.HTTP_403_FORBIDDEN)
        try:
            voucher = Voucher.objects.get(pk=pk)
            voucher.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Voucher.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class VoucherRoomViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = VoucherRom.objects.all()
    serializer_class = serializers.VoucherRomSerializer

    def get_queryset(self):
        queryset = self.queryset
        return queryset


class BookingViewSet(viewsets.ViewSet, generics.ListAPIView):
        queryset = Bookings.objects.all()
        serializer_class = serializers.BookingSerializer

        def get_queryset(self):
            queryset = self.queryset
            hotel_id = self.request.query_params.get('hotel_id')
            customer_id = self.request.query_params.get('customer_id')
            if hotel_id:
                queryset = queryset.filter(hotel=hotel_id)
            if customer_id:
                queryset = queryset.filter(customer=customer_id)
            return queryset

        @action(methods=['post'], url_path='booking', detail=False)
        def create_booking(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                hotel_room = HotelRom.objects.get(id=request.data['hotel_rom'])
                number_of_rooms_to_book = request.data['adults']

                if hotel_room.available_rooms < number_of_rooms_to_book:
                    return Response({"error": "Không đủ phòng có sẵn."}, status=status.HTTP_400_BAD_REQUEST)

                hotel_room.available_rooms -= number_of_rooms_to_book
                hotel_room.save()

                if request.data.get('voucher'):
                    voucher = Voucher.objects.get(id=request.data['voucher'])
                    voucher.current_uses = int(voucher.current_uses)
                    voucher.current_uses += 1
                    voucher.save()

                booking = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        @action(methods=['delete'], url_path='xoa_booking', detail=True)
        def xoa_booking(self, request, *args, **kwargs):
            try:
                booking = self.get_object()
            except Bookings.DoesNotExist:
                return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

            if booking.cancelable_until and timezone.now() <= booking.cancelable_until:
                booking.is_canceled = True
                booking.save()

                # Cập nhật số phòng khả dụng
                hotel_room = HotelRom.objects.get(id=booking.hotel_rom.id)
                hotel_room.available_rooms += 1
                hotel_room.save()

                return Response({"status": "Booking canceled and room availability updated."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": "Booking cannot be canceled."}, status=status.HTTP_400_BAD_REQUEST)


class BookingRoomViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = BookingRoom.objects.all()
    serializer_class = serializers.BookingRoomSerializer

    @action(methods=['post'], url_path='them_booking_room', detail=False)
    def them_booking_room(self, request):
        bookingroom = serializers.BookingRoomSerializer(data=request.data)
        if bookingroom.is_valid():
            bookingroom.save()
            return Response(bookingroom.data, status=status.HTTP_201_CREATED)
        return Response(bookingroom.errors, status=status.HTTP_400_BAD_REQUEST)


# API Thanh Toán MOMO
@csrf_exempt
def payment_view(request: HttpRequest):
    partnerCode = "MOMO"
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    requestId = f"{partnerCode}{int(time.time() * 1000)}"
    orderId = 'MM' + str(int(time.time() * 1000))
    orderInfo = "pay with MoMo"
    redirectUrl = "http://localhost:3000/"
    ipnUrl = "https://callback.url/notify"
    amount = request.headers.get('amount', '')
    requestType = "payWithATM"
    extraData = ""

    # Construct raw signature
    rawSignature = f"accessKey={accessKey}&amount={amount}&extraData={extraData}&ipnUrl={ipnUrl}&orderId={orderId}&orderInfo={orderInfo}&partnerCode={partnerCode}&redirectUrl={redirectUrl}&requestId={requestId}&requestType={requestType}"

    # Generate signature using HMAC-SHA256
    signature = hmac.new(secretKey.encode(), rawSignature.encode(), hashlib.sha256).hexdigest()

    # Create request body as JSON
    data = {
        "partnerCode": partnerCode,
        "accessKey": accessKey,
        "requestId": requestId,
        "amount": amount,
        "orderId": orderId,
        "orderInfo": orderInfo,
        "redirectUrl": redirectUrl,
        "ipnUrl": ipnUrl,
        "extraData": extraData,
        "requestType": requestType,
        "signature": signature,
        "lang": "vi"
    }

    # Send request to MoMo endpoint
    url = 'https://test-payment.momo.vn/v2/gateway/api/create'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)

    # Process response
    if response.status_code == 200:
        response_data = response.json()
        pay_url = response_data.get('payUrl')
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": f"Failed to create payment request. Status code: {response.status_code}"},
                            status=500)


# TẠO API THANH TOÁN BẰNG ZALO PAY
config = {
      "app_id": 2553,
      "key1": "PcY4iZIKFCIdgZvA6ueMcMHHUbRLYjPL",
      "key2": "kLtgPl8HHhfvMuDHPwKfgfsY4Ydm9eIz",
      "endpoint": "https://sb-openapi.zalopay.vn/v2/create"
}

@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        # Lấy thông tin từ yêu cầu của người dùng
        amount = request.headers.get('amount', '')  # Lấy amount từ header
        transID = random.randrange(1000000)
        # Xây dựng yêu cầu thanh toán
        order = {
            "app_id": config["app_id"],
            "app_trans_id": "{:%y%m%d}_{}".format(datetime.today(), transID),  # mã giao dich có định dạng yyMMdd_xxxx
            "app_user": "user123",
            "app_time": int(round(time.time() * 1000)),  # miliseconds
            "embed_data": json.dumps({}),
            "item": json.dumps([{}]),
            "amount": amount,
            "description": "Thanh Toán Vé Xe #" + str(transID),
            "bank_code": "",
        }

        # Tạo chuỗi dữ liệu và mã hóa HMAC
        data = "{}|{}|{}|{}|{}|{}|{}".format(order["app_id"], order["app_trans_id"], order["app_user"],
                                             order["amount"], order["app_time"], order["embed_data"], order["item"])
        order["mac"] = hmac.new(config['key1'].encode(), data.encode(), hashlib.sha256).hexdigest()

        # Gửi yêu cầu đến ZaloPay API
        try:
            response = urllib.request.urlopen(url=config["endpoint"], data=urllib.parse.urlencode(order).encode())
            result = json.loads(response.read())
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": "Only POST requests are allowed"})
