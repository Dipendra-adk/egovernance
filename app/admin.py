from django.contrib import admin
from app.models import Tender,Bid,Contact

# Register your models here.
admin.site.register(Tender)
admin.site.register(Bid)
admin.site.register(Contact)