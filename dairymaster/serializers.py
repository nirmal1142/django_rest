from rest_framework import serializers
from django.db.models import Sum
from dairymaster.models import DairyMaster , CompanyRate ,DairyToCompanyMilk,CompanyProfile , RetailSellMilk , RetailRate
import json
from account.models import User


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = '__all__'

class CompanyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyRate
        fields = '__all__'

class DairyToCompanyMilkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DairyToCompanyMilk
        fields = '__all__'

class RetailSellMilkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailSellMilk
        fields = '__all__'

class DairyMasterGetSerializer(serializers.ModelSerializer):
    company_rate = CompanyRateSerializer(many=True)
    dairy_to_company_milk = DairyToCompanyMilkSerializer(many=True)

    class Meta:
        model = DairyMaster
        fields = ['id','company_rate','dairy_to_company_milk' ,'date','shift','profit','description']

class DairyMasterSerializer(serializers.ModelSerializer):
    company_rate = CompanyRateSerializer(many=True)
    dairy_to_company_milk = DairyToCompanyMilkSerializer(many=True)

    class Meta:
        model = DairyMaster
        fields = ['id','company_rate','dairy_to_company_milk' ,'date','shift','profit','description']

    def create(self, validated_data):
        date = validated_data.get('date')
        shift = validated_data.get('shift')
        user = validated_data.get('user')
        dairy_master = DairyMaster.objects.filter(date=date,shift=shift,user=user)

        if dairy_master:
            raise serializers.ValidationError("Dairy Master Already Exists")
        else:
            company_rate_data = validated_data.pop('company_rate')
            dairy_to_company_milk_data = validated_data.pop('dairy_to_company_milk')
            dairy_master = DairyMaster.objects.create(**validated_data)

            for company_rate in company_rate_data:
                price = company_rate['liter'] * company_rate['rate'] * company_rate['fat']
                company_rate , created = CompanyRate.objects.get_or_create(rate=company_rate['rate'],milk_type=company_rate['milk_type'],liter=company_rate['liter'],fat=company_rate['fat'],price=price,mainId=dairy_master.id)
                dairy_master.company_rate.add(company_rate)

            for dairy_to_company_milk in dairy_to_company_milk_data:
                price = dairy_to_company_milk['liter'] * dairy_to_company_milk['rate'] * dairy_to_company_milk['fat']
                dairy_to_company_milk , created = DairyToCompanyMilk.objects.get_or_create(rate=dairy_to_company_milk['rate'],milk_type=dairy_to_company_milk['milk_type'],liter=dairy_to_company_milk['liter'],fat=dairy_to_company_milk['fat'],price=price,mainId=dairy_master.id)
                dairy_master.dairy_to_company_milk.add(dairy_to_company_milk)

            profite = dairy_master.company_rate.aggregate(Sum('price'))['price__sum'] - dairy_master.dairy_to_company_milk.aggregate(Sum('price'))['price__sum']
            dairy_master.profit = profite
            dairy_master.save()
            return dairy_master

    
class milkMonthlyReportSerializer(serializers.ModelSerializer):
    company_rate = CompanyRateSerializer(many=True)
    dairy_to_company_milk = DairyToCompanyMilkSerializer(many=True)

    class Meta:
        model = DairyMaster
        fields = ['id','company_rate','dairy_to_company_milk' ,'date','shift','profit','description']

        
class RetailRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailRate
        fields = ['id','rate','milk_type']

    def create(self , validated_data):
        milk_type = validated_data.get('milk_type')
        user = validated_data.get('user')

        retail_rate = RetailRate.objects.filter(milk_type=milk_type,user=user)

        if retail_rate:
            raise serializers.ValidationError("Retail Rate Already Exists")
        else:
            retail_rate = RetailRate.objects.create(**validated_data)
            return retail_rate

    def update(self , instance , validated_data):
        milk_type = validated_data.get('milk_type')
        rate = validated_data.get('rate')
        user = validated_data.get('user')

        retail_rate = RetailRate.objects.filter(milk_type=milk_type,user=user , rate=rate)

        if retail_rate:
            raise serializers.ValidationError("Retail Rate Already Exists")
        else:
            instance.rate = validated_data.get('rate')
            instance.milk_type = validated_data.get('milk_type')
            instance.save()
            return instance
