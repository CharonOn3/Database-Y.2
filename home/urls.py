from django.urls import path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home import views as home_views
urlpatterns = [
    path('',index, name= 'index'),
    
    path ("Contact",contact,name= 'contact'),
    path ("Blog",blog,name= 'blog'),
    path ("About",about,name= 'about'),
    path ("Garden",garden,name='garden'),
    path ("Sea",sea,name='sea'),
    path ("Pool",pool,name='pool'),
    path ("Detail",detail,name='detail'),
    path ("Report",report,name='report'),
    path ("Confirm",confirm,name='confirm'),
    path ("Show",show,name='show'),
    path ("Payment",payment,name='payment'),
    path ("Login",login,name='login'),
    path ("Signup",signup,name='signup'),


    #reserve
    path('Reservation', home_views.reservation, name='reservation'),
    path('Reservation/list', home_views.ReserveList.as_view(), name='reserve_list'),
    path('Reservation/detail/<str:pk>/<str:pk2>', home_views.ReserveDetail.as_view(), name='reserve_detail'),
    path('Reservation/create', home_views.ReserveCreate.as_view(), name='reserve_create'),
    path('Reservation/update/<str:pk>/<str:pk2>', home_views.ReserveUpdate.as_view(), name='reserve_update'),
    path('Reservation/report', home_views.ReserveReport.as_view(), name='reserve_report'),
    path('Reservation/Detail', home_views.detail, name='reserve_detail1'),
    path('Reservation/Detail/Payment', home_views.payment, name='reserve_payment'),


    #receipt
    path('Receipt_hotel', home_views.index, name='receipt'),
    path('Receipt_hotel/list', home_views.ReceiptHotelList.as_view(), name='receipt_list'),
    path('Receipt_hotel/detail/<str:pk>/<str:pk2>', home_views.ReceiptHotelDetail.as_view(), name='receipt_detail'),
    path('Receipt_hotel/create', home_views.ReceiptHotelCreate.as_view(), name='receipt_create'),
    path('Receipt_hotel/update/<str:pk>/<str:pk2>', home_views.ReceiptHotelUpdate.as_view(), name='receipt_update'),
    path('Receipt_hotel/report', home_views.ReceiptHotelReport.as_view(), name='receipt_report'),

    #receipt_line
    path('Receiptline', home_views.index, name='index'),
    path('Receiptline/list', home_views.ReceiptLineItemHotelList.as_view(), name='receiptline_list'),

    #payment
    path('Paymemt', home_views.index, name='index'),
    path('Payment/list', home_views.PaymentList.as_view(), name='payment_list'),

    #customer
    path('Customer', home_views.index, name='index'),
    path('Customer/list', home_views.CustomerHotelList.as_view(), name='customer_list'),
    path('Customer/create', home_views.CustomerHotelCreate.as_view(), name='customer_create'),

    #customer
    path('Room_type', home_views.index, name='index'),
    path('Room_type/list', home_views.RoomTypeList.as_view(), name='room_type_list'),
    ]
urlpatterns += staticfiles_urlpatterns()
