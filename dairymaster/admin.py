from django.contrib import admin
from dairymaster.models import DairyToCompanyMilk , CompanyRate, DairyMaster

# Register your models here.

admin.site.register(DairyMaster)
admin.site.register(DairyToCompanyMilk)
admin.site.register(CompanyRate)