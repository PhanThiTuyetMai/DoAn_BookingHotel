from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from . import routing

r = routers.DefaultRouter()
r.register('users', views.UserViewSet, 'users')
r.register('employees', views.EmployeeViewSet, 'employees')
r.register('customers', views.CustomerViewSet, 'customers')
r.register('roles', views.RoleViewSet, 'roles')
r.register('provinces', views.ProvinceViewSet, 'provinces')
r.register('hotels', views.HotelViewSet, 'hotels')
r.register('hotelrooms', views.HotelRoomViewSet, 'hotelrooms')
r.register('roomimages', views.RomImagesViewSet, 'roomimages')
r.register('comments', views.CommentViewSet, 'comments')
r.register('services', views.HotelServiceViewSet, 'services')
r.register('request', views.HotelRequestViewSet, 'request')
r.register('hotelimages', views.HotelImagesViewSet, 'hotelimages')
r.register('typeroom', views.TypeRoomViewSet, 'typeroom')
r.register('voucher', views.VoucherViewSet, 'voucher')
r.register('voucher_room', views.VoucherRoomViewSet, 'voucher_room')
r.register('booking', views.BookingViewSet, 'booking')
r.register('bookingroom', views.BookingRoomViewSet, 'bookingroom')

urlpatterns = [
    path('', include(r.urls)),
    path('payment/', views.payment_view, name='payment'),
    path('zalo/payment/', views.create_payment, name='zalopay'),
    path('api/hotels/search/', views.HotelViewSet.as_view({'get': 'search_hotels'}), name='search_hotels'),
]

websocket_urlpatterns = routing.websocket_urlpatterns
