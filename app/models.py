from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
# import uuid


class Tender(models.Model):
    CATEGORIES = [
        ('Goods Procurement', 'Goods Procurement'),
        ('Construction', 'Construction'),
        ('Research & Development', 'Research & Development'),
        ('HealthCare', 'HealthCare'),
        ('Electronics', 'Electronics'),
        ('Education and Training', 'Education and Training'),
        ('Waste Management','Waste Management'),
        ('Other', 'Other'),
    ]
    STATUS = [
        ('Pending', 'Pending'),
        ('Active','Active'),
        ('Closed', 'Closed'),
    ]
    # id = models.UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     editable=False
    # )
    
    category = models.CharField(max_length = 30, choices = CATEGORIES, default = 'Other')
    title = models.CharField(max_length=100)
    #image = models.ImageField(upload_to="uploads")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    baseprice = models.IntegerField()
    
    # Contractor info 
    contractor_company_name = models.CharField(max_length=200,default='Your Default Value')
    contractor_name = models.CharField(max_length=150)
    contractor_email = models.EmailField(max_length=200)
    contractor_phone = PhoneNumberField(region="NP", max_length=15)

    
    planning_phase1_date = models.DateField()
    planning_phase1_payment = models.IntegerField()
    planning_phase2_date = models.DateField()
    planning_phase2_payment = models.IntegerField()
    planning_final_date = models.DateField()
    planning_final_payment = models.IntegerField()
    
    terms_and_conditions = models.TextField()


    #owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tenders')
    status = models.CharField(max_length=7, choices=STATUS, default='Active')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_tenders')
    
    @property
    def is_closed(self):
        if self.deadline < timezone.now() and self.status != 'Closed':
            self.status = 'Closed' # update the status to closed
            self.save() # save the updated status
            return self.status == 'Closed'
        return False

    
    # @property
    # def is_closed(self):
    #     return self.deadline < timezone.now() and self.status != 'Closed'

    # def save(self, *args, **kwargs):
    #     if self.is_closed():
    #         self.status = 'Closed'
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.title  
    
    def get_absolute_url(self):
        return reverse("tender_detail", args=[str(self.id)])    

class Bidder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bidder_profile')
    company_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = PhoneNumberField(region="NP", max_length=13)
    address = models.TextField()
    
    def __str__(self):
        return self.user.username + " - " + self.company_name
    

class Bid(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidding_time = models.DateTimeField(auto_now = True)
    
    
    def __str__(self):
        return f"Bid for {self.tender.title} by {self.bidder.username}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name}"
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Bid win notification"    