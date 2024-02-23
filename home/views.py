from django.shortcuts import render
from django.shortcuts import render
from django.db.models.fields import NullBooleanField
from django.http import HttpResponse, response

from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.db.models import Max
from django.db import connection
from .models import *
import json
# Create your views here.

"""def index (request):
    chambres= Chambre.objects.all()
    catalogues= Catalogue.objects.all()
    testimonials = Testimonial.objects.all()
    render(request,'index.html',{'testimonial': testimonials})
    render (request,'index.html',{'catalogues': catalogues})
    return render(request,"index.html",{'chambres': chambres})
def reservation (request):
    return render(request, "reservation.html")
def contact(request):
    return  render (request, "contact.html")
def blog (request):
    chambres = Chambre.objects.all()
    return render (request, "blog.html",{'chambres': chambres})
def about(request):
    return render (request, 'about.html')"""

def index(request):
    data = {}
    return render(request, 'index.html', data)
 
class RoomList(View):
    def get(self, request):
        rooms = list(Room.objects.order_by('room_no').all().values())
        data = dict()
        data['rooms'] = rooms
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class RoomTypeList(View):
    def get(self, request):
        roomtypes =  list(RoomType.objects.order_by('room_type_id').all().values())
        data = dict()
        data['roomtypes'] = roomtypes
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class ReserveList(View):
    def get(self, request):
        reserves =  list(Reserve.objects.order_by('reserve_no').all().values())
        data = dict()
        data['reserves'] = reserves
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response
            
class ReserveLineItemList(View):
    def get(self, request):
        reserveslines =  list(ReserveLineItem.objects.order_by('reserve_no').all().values())
        data = dict()
        data['reserveslines'] = reserveslines
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response 
            
class CustomerHotelList(View):
    def get(self, request):
        customers = list(CustomerHotel.objects.all().values())
        data = dict()
        data['customers'] = customers
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class PaymentList(View):
    def get(self, request):
        payments = list(PaymentMethod.objects.order_by('payment_method').all().values())
        data = dict()
        data['payments'] = payments
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response
        
class ReceiptHotelList(View):
    def get(self, request):
        receipts = list(ReceiptHotel.objects.order_by('receipt_no').all().values())
        data = dict()
        data['receipts'] = receipts
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class ReceiptLineItemHotelList(View):
    def get(self, request):
        receiptlines = list(ReceiptLineItemHotel.objects.order_by('receipt_no').all().values())
        data = dict()
        data['receiptlines'] = receiptlines
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response    

class PromotionList(View):
    def get(self, request):
        discounts = list(Promotion.objects.order_by('discount').all().values())
        data = dict()
        data['discounts'] = discounts
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

#reservedetail
class ReserveDetail(View):
    def get(self, request, pk, pk2):
        reserve_no = pk + "/" + pk2

        reserve = list(Reserve.objects.select_related("customer_hotel").filter(reserve_no=reserve_no).values('reserve_no', 'reserve_date', 'customer_code', 'qty_room','total_price','vat','discount','amount_due','total_deposit'))
        reservelineitem = list(ReserveLineItem.objects.select_related('room_type').filter(reserve_no=reserve_no).order_by('room_no').values("room_no","room_type","unit_price","qty_day","total_price","check_in_date","check_out_date"))

        data = dict()
        data['reserve'] = reserve[0]
        data['reservelineitem'] = reservelineitem

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response
        
#receiptdetail
class ReceiptHotelDetail(View):
    def get(self, request, pk, pk2):
        receipt_no = pk + "/" + pk2

        receiptHotel = list(ReceiptHotel.objects.select_related("customer").filter(receipt_no=receipt_no).values('receipt_no', 'receipt_date', 'customer_code', 'payment_method','payment_reference','total_receipt','remarks'))
        receiptlineitemHotel = list(ReceiptLineItemHotel.objects.select_related('reserve_no').filter(receipt_no=receipt_no).order_by('item_no').values("item_no","receipt_no","reserve_no","room_no","reserve_date","reserve_full_amount","reserve_amount_remain","amount_paid_here"))

        data = dict()
        data['receiptHotel'] = receiptHotel[0]
        data['receiptlineitemHotel'] = receiptlineitemHotel

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

#CustomerHotelDetail
class CustomerHotelDetail(View):
    def get(self, request, pk):
        customer = get_object_or_404(CustomerHotel, pk=pk)
        data = dict()
        data['customers'] = model_to_dict(customer)
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

# *receipfrom, receiplinefrom, reservefrom, reservelinefrom
class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerHotel
        fields = '__all__'

class ReceiptHotelForm(forms.ModelForm):
    class Meta:
        model = ReceiptHotel
        fields = '__all__'

class ReceiptLineItemHotelForm(forms.ModelForm):
    class Meta:
        model = ReceiptLineItemHotel
        fields = '__all__'

class ReserveForm(forms.ModelForm):
    class Meta:
        model = Reserve
        fields = '__all__'

class ReserveLineItemForm(forms.ModelForm):
    class Meta:
        model = ReserveLineItem
        fields = '__all__'

#receipt: create,update,report
class ReceiptHotelCreate(View):
    def post(self, request):
        data = dict()
        request.POST = request.POST.copy()
        if ReceiptHotel.objects.count() != 0:
            receipt_no_max = ReceiptHotel.objects.aggregate(Max('receipt_no'))['receipt_no__max']
            next_receipt_no = receipt_no_max[0:3] + str(int(receipt_no_max[3:7])+1) + "/" + receipt_no_max[8:10]

        else:
            next_receipt_no = "RCT1001/21"
        request.POST['receipt_no'] = next_receipt_no
        request.POST['receipt_date'] = reFormatDateMMDDYYYY(request.POST['date'])
        request.POST['payment_thod'] = request.POST['payment_method']
        request.POST['total_receipt'] = reFormatNumber(request.POST['total_receipt'])
        request.POST['payment_reference'] = request.POST['payment_reference']
        request.POST['remarks'] = request.POST['remarks']

        form = ReceiptHotelForm(request.POST)
        
        if form.is_valid():
            receipt = form.save()

            dict_lineitem = json.loads(request.POST['lineitem'])
            for lineitem in dict_lineitem['lineitem']:
                reserve_no = Reserve.objects.get(pk=lineitem['reserve_no'])
                ReceiptLineItemHotel.objects.create(
                    receipt_no=receipt,
                    room_no=lineitem['room_no'],
                    reserve_no=reserve_no,
                    reserve_date=lineitem['reserve_date'],
                    reserve_full_amount=reFormatNumber(lineitem['reserve_full_amount']),
                    reserve_amount_remain=reFormatNumber(lineitem['reserve_amount_remain']),
                    amount_paid_here=reFormatNumber(lineitem['amount_paid_here'])
                )

            data['receipt'] = model_to_dict(receipt)
        else:
            data['error'] = 'form not valid!'

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response
        
class ReceiptHotelUpdate(View):
    def post(self, request, pk, pk2):
        receipt_no = pk + "/" + pk2
        data = dict()
        receipt = ReceiptHotel.objects.get(pk=receipt_no)
        request.POST = request.POST.copy()
        request.POST['receipt_no'] = receipt_no
        request.POST['receipt_date'] = reFormatDateMMDDYYYY(request.POST['date'])
        request.POST['payment_thod'] = request.POST['payment_method']
        request.POST['total_receipt'] = reFormatNumber(request.POST['total_receipt'])
        request.POST['payment_reference'] = request.POST['payment_reference']
        request.POST['remarks'] = request.POST['remarks']
        
        form = ReceiptHotelForm(instance=receipt, data=request.POST)
        if form.is_valid():
            receipt = form.save()

            ReceiptLineItemHotel.objects.filter(receipt_no=receipt_no).delete()

            dict_lineitem = json.loads(request.POST['lineitem'])
            for lineitem in dict_lineitem['lineitem']:
                reserve_no = Reserve.objects.get(pk=lineitem['reserve_no'])
                ReceiptLineItemHotel.objects.create(
                    receipt_no=receipt,
                    room_no=lineitem['room_no'],
                    reserve_no=reserve_no,
                    reserve_date=lineitem['reserve_date'],
                    reserve_full_amount=reFormatNumber(lineitem['reserve_full_amount']),
                    reserve_amount_remain=reFormatNumber(lineitem['reserve_amount_remain']),
                    amount_paid_here=reFormatNumber(lineitem['amount_paid_here'])
                )

            data['receipt'] = model_to_dict(receipt)
        else:
            data['error'] = 'form not valid!'

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class ReceiptHotelReport(View):
    def get(self, request):

        with connection.cursor() as cursor:
            cursor.execute('SELECT rh.receipt_no as "Receipt No", rh.receipt_date as "Date" ,'
                            'rh.customer_code as "Customer Code",'
                            'rh.payment_method as "Payment Method" , rh.payment_reference as "Payment Reference",'
                            'rh.total_receipt as "Total Received", rh.remarks as "Remarks" '
                            'FROM receipt_hotel rh JOIN customer_hotel ch '
                            'ON rh.customer_code = ch.customer_code '
                            'ORDER BY rh.receipt_no')
        
            row = dictfetchall(cursor)
            column_name = [col[0] for col in cursor.description]

        data = dict()
        data['column_name'] = column_name
        data['data'] = row
        
        #return JsonResponse(data)
        return render(request, 'receipt_hotel/report.html', data)


#reserve: create,update,report
class ReserveCreate(View):
    def post(self, request):
        data = dict()
        request.POST = request.POST.copy()
        if Reserve.objects.count() != 0:
            reserve_no_max = Reserve.objects.aggregate(Max('reserve_no'))['reserve_no__max']
            next_reserve_no = reserve_no_max[0:2] + str(int(reserve_no_max[2:6])+1) + "/" + reserve_no_max[7:9]
        else:
            next_reserve_no = "RS1001/21"
        print("aa")
        request.POST['reserve_no'] = next_reserve_no
        request.POST['reserve_date'] = reFormatDateMMDDYYYY(request.POST['reserve_date'])
        request.POST['qty_room'] = reFormatNumber(request.POST['qty_room'])
        request.POST['total_price'] = reFormatNumber(request.POST['total_price'])
        request.POST['vat'] = reFormatNumber(request.POST['vat'])
        request.POST['discount'] = reFormatNumber(request.POST['discount'])
        request.POST['amount_due'] = reFormatNumber(request.POST['amount_due'])
        request.POST['total_deposit'] = reFormatNumber(request.POST['total_deposit'])


        form = ReserveForm(request.POST)
        if form.is_valid():
            reserve = form.save()

            dict_lineitem = json.loads(request.POST['lineitem'])
            for lineitem in dict_lineitem['lineitem']:
                room_type = RoomType.objects.get(pk=lineitem['room_type'])
                ReserveLineItem.objects.create(
                    reserve_no=reserve,
                    room_no=lineitem['room_no'],
                    room_type=room_type,
                    unit_price=reFormatNumber(lineitem['unit_price']),
                    qty_day=reFormatNumber(lineitem['qty_day']),
                    total_price=reFormatNumber(lineitem['total_price']),
                    check_in_date = reFormatDateMMDDYYYY(lineitem['check_in_date']),
                    check_out_date = reFormatDateMMDDYYYY(lineitem['check_out_date']),
                )

            data['reserve'] = model_to_dict(reserve)
        else:
            data['error'] = 'form not valid!'

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class ReserveReport(View):
    def get(self, request):

        with connection.cursor() as cursor:
            cursor.execute ('SELECT r.reserve_no as "Reserve No", r.reserve_date as "Date" ,'
                            'r.customer_code as "Customer Code", r.qty_room as "Quantity Room",'
                            'r.total_price as "Total Price", r.vat as "Vat",'
                            'r.discount as "Discount", r.amount_due as "Amount Due", r.total_deposit as "Total Deposit"'
                            'FROM reserve r JOIN customer_hotel ch '
                            'ON r.customer_code = ch.customer_code '
                            'ORDER BY r.reserve_no')
        
            row = dictfetchall(cursor)
            column_name = [col[0] for col in cursor.description]

        data = dict()
        data['column_name'] = column_name
        data['data'] = row
        
        #return JsonResponse(data)
        return render(request, 'reserve/report.html', data)

@method_decorator(csrf_exempt, name='dispatch')
class ReserveUpdate(View):
    def post(self, request, pk, pk2):
        invoice_no = pk + "/" + pk2
        data = dict()
        reserve = Reserve.objects.get(pk=invoice_no)
        request.POST = request.POST.copy()
        request.POST['reserve_no'] = invoice_no
        request.POST['reserve_date'] = reFormatDateMMDDYYYY(request.POST['reserve_date'])
        request.POST['qty_room'] = reFormatNumber(request.POST['qty_room'])
        request.POST['total_price'] = reFormatNumber(request.POST['total_price'])
        request.POST['vat'] = reFormatNumber(request.POST['vat'])
        request.POST['discount'] = reFormatNumber(request.POST['discount'])
        request.POST['amount_due'] = reFormatNumber(request.POST['amount_due'])
        request.POST['total_deposit'] = reFormatNumber(request.POST['total_deposit'])

        form = ReserveForm(instance=reserve, data=request.POST)
        if form.is_valid():
            reserve = form.save()

            ReserveLineItem.objects.filter(reserve_no=reserve).delete()

            dict_lineitem = json.loads(request.POST['lineitem'])
            for lineitem in dict_lineitem['lineitem']:
                room_type = RoomType.objects.get(pk=lineitem['room_type'])
                ReserveLineItem.objects.create(
                    reserve_no=reserve,
                    room_no=lineitem['room_no'],
                    room_type=room_type,
                    unit_price=reFormatNumber(lineitem['unit_price']),
                    qty_day=reFormatNumber(lineitem['qty_day']),
                    total_price=reFormatNumber(lineitem['total_price']),
                    check_in_date = reFormatDateMMDDYYYY(lineitem['check_in_date']),
                    check_out_date = reFormatDateMMDDYYYY(lineitem['check_out_date']),
                )

            data['reserve'] = model_to_dict(reserve)
        else:
            data['error'] = 'form not valid!'

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class CustomerHotelCreate(View):
    def post(self, request):
        print(request)
        data = dict()
        request.POST = request.POST.copy()
        
        if CustomerHotel.objects.count() != 0:
            customer_code_max = CustomerHotel.objects.aggregate(Max('customer_code'))['customer_code__max']
            next_customer_code = customer_code_max[0:2] + str(int(customer_code_max[2:5])+1)
        else:
            next_customer_code = "LN101"
        request.POST['customer_code'] = next_customer_code
        request.POST['lastname'] = request.POST['surname']
        request.POST['phone'] = request.POST['phone']
        request.POST['email'] = request.POST['email']
        del request.POST['csrfmiddlewaretoken']
        del request.POST['surname']
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()

            """dict_lineitem = json.loads(request.POST['lineitem'])
            for lineitem in dict_lineitem['lineitem']:
                product_code = Product.objects.get(pk=lineitem['product_code'])
                InvoiceLineItem.objects.create(
                    invoice_no=invoice,
                    item_no=lineitem['item_no'],
                    product_code=product_code,
                    unit_price=reFormatNumber(lineitem['unit_price']),
                    quantity=reFormatNumber(lineitem['quantity']),
                    product_total=reFormatNumber(lineitem['product_total'])
                )"""

            data['customer'] = model_to_dict(customer)
        else:
            data['error'] = 'form not valid!'

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response


class CustomerHotelUpdate(View):
    def post(self, request, pk):
        customer_code = pk
        data = dict()
        customer = CustomerHotel.objects.get(pk=customer_code)
        request.POST = request.POST.copy()
        request.POST['customer_code'] = customer_code
        request.POST['customer_name'] = request.POST['customer_name'] 
        request.POST['customer_lastname'] = request.POST['customer_lastname']
        request.POST['phone_number'] = request.POST['phone_number']
        request.POST['email'] = request.POST['email']

        form = CustomerForm(instance=customer, data=request.POST)
        if form.is_valid():
            customer = form.save()

            """ReserveLineItem.objects.filter(reserve_no=reserve).delete()

            dict_lineitem = json.loads(request.POST['lineitem'])
            for lineitem in dict_lineitem['lineitem']:
                room_type = RoomType.objects.get(pk=lineitem['room_type'])
                ReserveLineItem.objects.create(
                    reserve_no=reserve,
                    room_no=lineitem['room_no'],
                    room_type=room_type,
                    unit_price=reFormatNumber(lineitem['unit_price']),
                    qty_day=reFormatNumber(lineitem['qty_day']),
                    total_price=reFormatNumber(lineitem['total_price']),
                    check_in_date = reFormatDateMMDDYYYY(lineitem['check_in_date']),
                    check_out_date = reFormatDateMMDDYYYY(lineitem['check_out_date']),
                )"""
            data['customer'] = model_to_dict(customer)
        else:
            data['error'] = 'form not valid!'

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response



def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [name[0].replace(" ", "_").lower() for name in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def reFormatDateMMDDYYYY(ddmmyyyy):
        if (ddmmyyyy == ''):
            return ''
        return ddmmyyyy[3:5] + "/" + ddmmyyyy[:2] + "/" + ddmmyyyy[6:]

def reFormatNumber(str):
        if (str == ''):
            return ''
        return str.replace(",", "")

def reFormatDateYYYYMMDD(ddmmyyyy):
        if (ddmmyyyy == ''):
            return ''
        return ddmmyyyy[6:] + "-" + ddmmyyyy[3:5] + "-" + ddmmyyyy[:2]
# Create your views here.

def index (request):
    return render(request,"index.html")
def reservation (request):
    return render(request, "reservation.html")
def contact(request):
    return  render (request, "contact.html")
def blog (request):
    return render (request, "blog.html")
def about(request):
    return render (request, 'about.html')
def allroom(request):
    return render (request, "allroom.html")
def garden(request):
    return render(request, "garden.html")
def sea(request):
    return render(request, "sea.html")
def pool(request):
    return render(request, "pool.html")
def detail(request):
    return render(request, "detail.html")
def report(request):
    return render(request, "report.html")
def confirm(request):
    return render(request, "confirm.html")
def show(request):
    return render(request, "show.html")
def payment(request):
    return render(request, "payment.html")
def login(request):
    return render(request, "login.html")
def signup(request):
    return render(request, "signup.html")
