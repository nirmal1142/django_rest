from django.db import models
from django.utils import timezone
import uuid
# from djangoauthapi.account.models import User
import sys
from djangoauthapi.settings import AUTH_USER_MODEL
from account.models import User
# Create your models here.


class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    company_email = models.EmailField(blank=True, null=True)
    company_phone = models.CharField(max_length=20, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    company_logo = models.ImageField(upload_to='company_logo/', blank=True, null=True)
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_created_at = models.DateTimeField(auto_now_add=True)
    company_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name





class DairyToCompanyMilk(models.Model):
    # dairy_id = models.ForeignKey(DairyMaster, on_delete=models.CASCADE)
    milk_type = models.CharField(max_length=20, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    liter = models.FloatField(blank=True, null=True)
    fat = models.FloatField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    mainId = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.milk_type


class CompanyRate(models.Model):
    # dairy_id = models.ForeignKey(DairyMaster, on_delete=models.CASCADE)
    milk_type = models.CharField(max_length=20, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    liter = models.FloatField(blank=True, null=True)
    fat = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mainId = models.CharField(blank=True, null=True,max_length=100)

    def __str__(self):
        return self.milk_type

class RetailSellMilk(models.Model):
    liter = models.FloatField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.milk_type


class DairyMaster(models.Model):
    date = models.DateField(default=timezone.now)
    shift = models.CharField(max_length=10, blank=True, null=True)
    profit = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    dairy_to_company_milk = models.ManyToManyField(DairyToCompanyMilk ,related_name='dairy_to_company_milk')
    company_rate = models.ManyToManyField(CompanyRate, related_name='company_rate')
    # user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True , blank=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.shift

class RetailRate(models.Model):
    milk_type = models.CharField(max_length=50, blank=False, null=False)
    rate = models.FloatField(blank=False, null=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True , blank=True)
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.milk_type





