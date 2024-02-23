from django.db import models



# Create your models here.


class Data(models.Model):
    key = models.CharField(max_length=10,primary_key=True)
    value = models.CharField(max_length=100)

class Room(models.Model):
    room_no = models.CharField(max_length=10,primary_key=True)
    room_type = models.CharField(max_length=100)
    floor = models.CharField(max_length=10)
    views = models.CharField(max_length=100)
    class Meta:
        db_table = "room"
        managed = False
    def __str__(self):
        return self.room_no

class RoomType(models.Model):
    room_type_id = models.CharField(max_length=10,primary_key=True)
    room_type = models.CharField(max_length=100)
    number_of_customer = models.IntegerField()
    price = models.FloatField(null=True, blank=True)
    description_room = models.CharField(max_length=100)
    class Meta:
        db_table = "room_type"
        managed = False
    def __str__(self):
        return self.room_type_id

class Reserve(models.Model):
    reserve_no = models.CharField(max_length=10,primary_key=True)
    reserve_date = models.DateField()
    customer_code = models.CharField(max_length=10)
    qty_room = models.IntegerField()
    total_price = models.FloatField(null=True, blank=True)
    vat = models.FloatField(null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)
    amount_due = models.FloatField(null=True, blank=True)
    total_deposit = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = "reserve"
        managed = False
    def __str__(self):
        return "%s %s" % (self.reserve_no, self.reserve_date)
    
class ReserveLineItem(models.Model):
    reserve_no = models.CharField(max_length=100,primary_key=True)
    room_no = models.ForeignKey(Room, on_delete=models.CASCADE, db_column='room_no')
    room_type = models.CharField(max_length=100)
    unit_price = models.FloatField(null=True,blank=True)
    qty_day = models.FloatField(null=True,blank=True)
    total_price = models.FloatField(null=True,blank=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    class Meta:
        db_table = "reserve_line_item"
        unique_together = (("reserve_no", "room_no"),)
        managed = False
    def __str__(self):
        return '{"reserve_no":"%s","room_no":"%s","room_type":"%s","unit_price":%s,"qty_day":"%s","total_price":"%s","check_in_date":"%s","check_out_date":"%s"}' % (self.reserve_no, self.room_no, self.room_type, self.unit_price, self.qty_day, self.total_price, self.check_in_date, self.check_out_date)

class CustomerHotel(models.Model):
    customer_code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=20, null=True, blank=True)
    class Meta:
        db_table = "customer_hotel"
        managed = False
    def __str__(self):
        return '{"customer_code":"%s","name":"%s","lastname":"%s","phone":"%s","email":%s}' % (self.customer_code, self.name, self.lastname, self.phone, self.email)

class PaymentMethod(models.Model):
    payment_method = models.CharField(max_length=10,primary_key=True)
    description = models.CharField(max_length=100) 
    class Meta:
        db_table = "payment_method"
        managed = False
    def __str__(self):
        return self.payment_method
        
class ReceiptHotel(models.Model):
    receipt_no = models.CharField(max_length=10, primary_key=True)
    receipt_date = models.DateField(null=True)
    customer_code = models.ForeignKey(CustomerHotel, on_delete=models.CASCADE, db_column='customer_code')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, db_column='payment_method')
    payment_reference = models.CharField(max_length=100, null=True, blank=True)
    total_receipt = models.FloatField(null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        db_table = "receipt_hotel"
        managed = False
    def __str__(self):
        return "%s %s" % (self.receipt_no, self.date)


class ReceiptLineItemHotel(models.Model):
    receipt_no = models.ForeignKey(ReceiptHotel, primary_key=True, on_delete=models.CASCADE, db_column='receipt_no')
    item_no = models.IntegerField()
    room_no =  models.ForeignKey(Room, on_delete=models.CASCADE, db_column='room_no')
    reserve_no = models.ForeignKey(Reserve, on_delete=models.CASCADE, db_column='reserve_no')
    reserve_date = models.DateField(null=True)
    reserve_full_amount = models.FloatField(null=True, blank=True)
    reserve_amount_remain = models.FloatField(null=True, blank=True)
    amount_paid_here =  models.FloatField(null=True, blank=True)
    class Meta:
        db_table = "receipt_line_item_hotel"
        unique_together = (("receipt_no", "item_no"),)
        managed = False
    def __str__(self):
        return '{"receipt_no":"%s","item_no":"%s","room_no":"%s","reserve_no":"%s","reserve_date":%s,"reserve_full_amount":"%s","reserve_amount_remain":"%s","amount_paid_here":"%s"}' % (self.receipt_no, self.item_no, self.room_no, self.reserve_no, self.reserve_date, self.reserve_full_amount, self.reserve_amount_remain,self.amount_paid_here)


class Promotion(models.Model):
    discount = models.FloatField(primary_key=True)
    event = models.CharField(max_length=100, null=True)
    special_event = models.CharField(max_length=100, null=True)
    event_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = "discount"
        managed = False
    def __str__(self):
        return "%s %s" % (self.discount)



# Create your models here.


class Chambre(models.Model):
    nom = models.CharField(max_length=20)
    prix = models.IntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='media/pics')
    disponibilité = models.BooleanField(default=True)

    def __str__(self):
        return self.nom
class Catalogue(models.Model):
    image = models.ImageField(upload_to='pics')
class Testimonial(models.Model):
    nom = models.CharField(max_length=20)
    avis = models.TextField()
    image = models.ImageField(upload_to='media/pics')
    def __str__(self):
        return self.nom
class Reservation(models.Model):
    Name = models.CharField(max_length=20)
    Phone = models.IntegerField(default=0)
    Email = models.EmailField(max_length=40)
    Date_Check_In = models.DateField(auto_now=False)
    Date_Check_Out  = models.DateField(auto_now=False)
    Adulte = models.IntegerField (default=0)
    Children = models.IntegerField(default=0)
    Note = models.TextField()
    def __str__(self):
        return self.Name
