from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(Stock)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Mechanic)