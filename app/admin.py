from django.contrib import admin
from app.models import Tender,Bid,Contact,Bidder

# Register your models here.
admin.site.register(Tender)
admin.site.register(Bid)
admin.site.register(Bidder)
admin.site.register(Contact)