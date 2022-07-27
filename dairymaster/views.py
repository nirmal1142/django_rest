from django.shortcuts import render
from django.http import HttpResponse
from dairymaster.serializers import DairyMasterGetSerializer,DairyMasterSerializer,milkMonthlyReportSerializer,RetailRateSerializer
from rest_framework.decorators import api_view  ,renderer_classes , permission_classes
from rest_framework import status
from dairymaster.renderers import UserRender
from rest_framework.response import Response
from rest_framework.views import APIView
from dairymaster.models import DairyMaster ,CompanyProfile,RetailRate ,CompanyRate,DairyToCompanyMilk
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters
# from rest_framework.pagination import PageNumberPagination
import json
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from account.models import User
from uuid import UUID
from .pagination import DairyMasterPagination
import datetime
from rest_framework import fields, generics, permissions, views
from src.utils.pagination import StandardResultsSetPagination
from twilio.rest import Client
from django.conf import settings


def send_sms(message,phone_number):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=settings.TWILIO_NUMBER,
        to=phone_number
    )
    return message.sid


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }

@api_view(['GET', 'POST'])
@renderer_classes([UserRender])
@permission_classes([IsAuthenticated])
def daily_milk_details_add(request , format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        user = request.user.id
        serializer = DairyMasterGetSerializer(DairyMaster.objects.filter(user=user), many=True)
        if serializer.data:
            data ={
                'status':'success',
                'data':serializer.data,
                'count':len(serializer.data)
            }
            return Response(data , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        data = request.data
        data['user'] = request.user.id
        searializer = DairyMasterSerializer(data=data)
        if searializer.is_valid(raise_exception=True):
            searializer.save()
            data = {
                'message': 'Daily Milk Details Added Successfully',
                'status': 'success',
                # 'data': searializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(searializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DailyMilkDetailGetById(APIView):
    def get(self, request, pk, format=None):
        dairy_master = DairyMaster.objects.get(pk=pk)
        serializer = DairyMasterSerializer(dairy_master)
        if serializer.data:
            data ={
                'status':'success',
                'data':serializer.data
            }
            return Response(data , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DairyMasterFindByDate(APIView):
    def get(self, request, format=None):
        dairy_master = DairyMaster.objects.filter(date=request.query_params.get('date'))
        serializer = DairyMasterSerializer(dairy_master, many=True)
        if serializer.data:
            data ={
                'status':'success',
                'data':serializer.data
            }
            return Response(data , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@renderer_classes([UserRender])
def daily_milk_details_update_delete(request, format=None):

    """
    Retrieve, update or delete a code snippet.
    """
    try:
        if request.query_params.get('id'):
            dairy_master = DairyMaster.objects.get(pk=request.query_params.get('id'))
        elif request.query_params.get('date'):
            dairy_master = DairyMaster.objects.filter(date=request.query_params.get('date'))
        else:
            dairy_master = DairyMaster.objects.all()
    except DairyMaster.DoesNotExist:
        return Response({'message':'not found'},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        dairy_master = DairyMaster.objects.get(id=request.query_params.get('id'))
        dairy_master.delete()
        data = {
            'message': 'Daily Milk Details Deleted Successfully',
            'status': 'success'
        }
        return Response(data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([UserRender])
def daily_milk_details_get_by_month(request, format=None):
    pass





class DairyMasterGetByManyDate(APIView):
    renderer_clssses = [UserRender]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            if request.data:
                dairy_master = DairyMaster.objects.filter(date__in=request.data, user=request.user.id)
            else:
                dairy_master = DairyMaster.objects.filter(user=request.user.id)
        except DairyMaster.DoesNotExist:
            return Response({'message':'not found'},status=status.HTTP_404_NOT_FOUND)
        if dairy_master not in []:
            serializer = DairyMasterGetSerializer(dairy_master, many=True)
            data ={
                'status':'success',
                'data':serializer.data,
                'count':len(serializer.data)
            }
            return Response(data , status=status.HTTP_200_OK)

class DairyMasterGetAll(generics.ListAPIView):
    serializer_class = milkMonthlyReportSerializer
    renderer_classes = [UserRender]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


    def get(self, request, format=None):
        try:
            dairy_master = DairyMaster.objects.filter(user=request.user.id)
        except DairyMaster.DoesNotExist:
            return Response({'message':'not found'},status=status.HTTP_404_NOT_FOUND)
        if dairy_master not in []:
            serializer = DairyMasterGetSerializer(dairy_master, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                paginatorData = self.paginate_queryset(serializer.data)
            else:
                paginatorData = serializer.data
            data ={
                'status':'success',
                'data':paginatorData,
                'count':len(paginatorData),
                'total_count':len(serializer.data)
            }
            return Response(data , status=status.HTTP_200_OK)

        # try:
        #     dairy_master = DairyMaster.objects.filter(user=request.user.id)
        # except DairyMaster.DoesNotExist:
        #     return Response({'message':'not found'},status=status.HTTP_404_NOT_FOUND)
        # if dairy_master not in []:
        #     serializer = DairyMasterGetSerializer(dairy_master, many=True)
        #     data ={
        #         'status':'success',
        #         'data':serializer.data,
        #         'count':len(serializer.data)
        #     }
        #     return Response(data , status=status.HTTP_200_OK)


class MonthlyReportView(generics.ListAPIView):
    serializer_class = milkMonthlyReportSerializer
    renderer_classes = [UserRender]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            if request.query_params.get('date'):
                date = request.query_params.get('date')
                date = datetime.datetime.strptime(date, "%Y-%m-%d")
                date = date.date()
                dairy_master = DairyMaster.objects.filter(date__month=date.month, date__year=date.year, user=request.user.id)
            else:
                dairy_master = []
        except DairyMaster.DoesNotExist:
            return Response({'message':'not found'},status=status.HTTP_404_NOT_FOUND)
        if dairy_master not in []:
            serializer = milkMonthlyReportSerializer(dairy_master, many=True)
            profit = 0
            for i in serializer.data:
                profit += i['profit']


            ######  Dairy to company data

            dairy_to_company_total_liters = 0
            for i in serializer.data:
                for j in i['dairy_to_company_milk'] :
                    dairy_to_company_total_liters += j['liter']

            dairy_to_company_total_amount = 0
            for i in serializer.data:
                for j in i['dairy_to_company_milk'] :
                    dairy_to_company_total_amount += j['price']

            max_fat = 0
            for i in serializer.data:
                for j in i['dairy_to_company_milk'] :
                    if j['fat'] > max_fat:
                        max_fat = j['fat']

            ######  Company to dairy data
            
            company_to_dairy_total_liters = 0
            for i in serializer.data:
                for j in i['company_rate'] :
                    company_to_dairy_total_liters += j['liter']

            company_to_dairy_total_amount = 0
            for i in serializer.data:
                for j in i['company_rate'] :
                    company_to_dairy_total_amount += j['price']

            max_fat_company = 0
            for i in serializer.data:
                for j in i['company_rate'] :
                    if j['fat'] > max_fat_company:
                        max_fat_company = j['fat']
                    

            dairy_data = {
                'total_liters':dairy_to_company_total_liters,
                'total_amount':dairy_to_company_total_amount,
                'max_fat':max_fat
            }
            company_data = {
                'total_liters':company_to_dairy_total_liters,
                'total_amount':company_to_dairy_total_amount,
                'max_fat':max_fat_company
            }
            profit ={
                'profit':profit,
                'liter_profit': company_to_dairy_total_liters - dairy_to_company_total_liters
            }
            data ={
                'status':'success',
                'data':serializer.data,
                "dairy_data":dairy_data,
                "company_data":company_data,
                'profit':profit,
                'count':len(serializer.data)
            }
            return Response(data , status=status.HTTP_200_OK)

class GetAllReportsCardView(generics.RetrieveAPIView):
    serializer_class = milkMonthlyReportSerializer
    renderer_classes = [UserRender]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            dairy_master = DairyMaster.objects.filter(user=request.user.id)
        except DairyMaster.DoesNotExist:
            return Response({'message':'not found'},status=status.HTTP_404_NOT_FOUND)
        if dairy_master not in []:
            serializer = milkMonthlyReportSerializer(dairy_master, many=True)
            all_data = serializer.data
            today = datetime.datetime.now()
            today = today.date()
            strDate = today.strftime("%Y-%m-%d")
            strMonth = today.strftime("%Y-%m")
            strYear = today.strftime("%Y")

            today_data = []
            for i in all_data:
                if i['date'] == strDate:
                    today_data.append(i)

            monthly_data = []
            for i in all_data:
                if i['date'].startswith(strMonth):
                    monthly_data.append(i)

            yearly_data = []
            for i in all_data:
                if i['date'].startswith(strYear):
                    yearly_data.append(i)

            today_profit = 0
            for i in today_data:
                today_profit += i['profit']

            monthly_profit = 0
            for i in monthly_data:
                monthly_profit += i['profit']

            yearly_profit = 0
            for i in yearly_data:
                yearly_profit += i['profit']

            total_profit = 0
            for i in all_data:
                total_profit += i['profit']

            dairy_to_company_total_liters = 0
            for i in all_data:
                for j in i['dairy_to_company_milk'] :
                    dairy_to_company_total_liters += j['liter']

            dairy_to_company_total_amount = 0
            for i in all_data:
                for j in i['dairy_to_company_milk'] :
                    dairy_to_company_total_amount += j['price']

            company_to_dairy_total_liters = 0
            for i in all_data:
                for j in i['company_rate'] :
                    company_to_dairy_total_liters += j['liter']

            company_to_dairy_total_amount = 0
            for i in all_data:
                for j in i['company_rate'] :
                    company_to_dairy_total_amount += j['price']

            dairy_to_company_monthly_liters = 0
            for i in monthly_data:
                for j in i['dairy_to_company_milk'] :
                    dairy_to_company_monthly_liters += j['liter']

            dairy_to_company_monthly_amount = 0
            for i in monthly_data:
                for j in i['dairy_to_company_milk'] :
                    dairy_to_company_monthly_amount += j['price']

            company_to_dairy_monthly_liters = 0
            for i in monthly_data:
                for j in i['company_rate'] :
                    company_to_dairy_monthly_liters += j['liter']

            company_to_dairy_monthly_amount = 0
            for i in monthly_data:
                for j in i['company_rate'] :
                    company_to_dairy_monthly_amount += j['price']

            data ={
                'status':'success',
                'today_profit':today_profit,
                'monthly_profit':monthly_profit,
                'yearly_profit':yearly_profit,
                'total_profit':total_profit,
                'dairy_to_company_total_liters':dairy_to_company_total_liters,
                'dairy_to_company_total_amount':dairy_to_company_total_amount,
                'company_to_dairy_total_liters':company_to_dairy_total_liters,
                'company_to_dairy_total_amount':company_to_dairy_total_amount,
                'dairy_to_company_monthly_liters':dairy_to_company_monthly_liters,
                'dairy_to_company_monthly_amount':dairy_to_company_monthly_amount,
                'company_to_dairy_monthly_liters':company_to_dairy_monthly_liters,
                'company_to_dairy_monthly_amount':company_to_dairy_monthly_amount,
                'count':len(serializer.data)
            }
            return Response(data , status=status.HTTP_200_OK)


class MilkProfitByMonth(APIView):
    renderer_classes = [UserRender]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            if request.query_params.get('month'):
                dairy_master = DairyMaster.objects.filter(date__month=request.query_params.get('month'), user=request.user.id)
            else:
                dairy_master = DairyMaster.objects.filter(user=request.user.id)
        except DairyMaster.DoesNotExist:
            return Response({'message':'not found'},status=status.HTTP_404_NOT_FOUND)
        if dairy_master not in []:
            serializer = DairyMasterGetSerializer(dairy_master, many=True)
            data ={
                'status':'success',
                'data':serializer.data,
                'count':len(serializer.data)
            }
            return Response(data , status=status.HTTP_200_OK)


class RetailRateView(APIView):
    renderer_classes = [UserRender]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            retail_rate = RetailRate.objects.filter(user=request.user.id)
            print("retail_rate",retail_rate)
        except RetailRate.DoesNotExist:
            return Response({'message':'not found'},status=status.HTTP_404_NOT_FOUND)
        if retail_rate not in []:
            serializer = RetailRateSerializer(retail_rate, many=True)
            data ={
                'status':'success',
                'data':serializer.data,
                'count':len(serializer.data)
            }
            return Response(data , status=status.HTTP_200_OK)
    def post(self, request, format=None):
        serializer = RetailRateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            retail_rate = RetailRate.objects.get(user=request.user.id , milk_type = request.data['milk_type'])
        except RetailRate.DoesNotExist:
            return Response({'message':'not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = RetailRateSerializer(retail_rate, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            retail_rate = RetailRate.objects.get(user=request.user.id , id=request.query_params.get('id'))
        except RetailRate.DoesNotExist:
            return Response({'message':'not found'},status=status.HTTP_404_NOT_FOUND)
        retail_rate.delete()
        return Response({'message':"success"},status=status.HTTP_200_OK)
        

class DairyMasterUpdateView(APIView):
    renderer_classes = [UserRender]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            if request.query_params.get('id'):
                dairy_master = DairyMaster.objects.filter(id=request.query_params.get('id'))
            else: 
                dairy_master = DairyMaster.objects.filter(user=request.user.id)
        except DairyMaster.DoesNotExist:
            return Response({'message':'not found'},status=status.HTTP_404_NOT_FOUND)
        if dairy_master not in []:
            serializer = DairyMasterGetSerializer(dairy_master, many=True)
            data ={
                'status':'success',
                'data':serializer.data,
                'count':len(serializer.data)
            }
            return Response(data , status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = DairyMasterSerializer(data=request.data)
        user = User.objects.get(id=request.user.id)
        if serializer.is_valid():
            serializer.save(user=request.user)

            sms_body = "Dear  " + user.name + ", \n\n " + "Your Today's Profit is  "  + str(serializer.data['profit']) + " \n\n " + "Date : " + str(serializer.data['date']) + " \n\n " + "Shift : " + str(serializer.data['shift']) + " \n\n " + "Thanks & Regards \n\n " + "Dairy Farm"

            # send_sms(sms_body,"+919662169628" )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            dairy_master = DairyMaster.objects.get(user=request.user.id , id=request.query_params.get('id'))
        except DairyMaster.DoesNotExist:
            return Response({'message':'not found'},status=status.HTTP_404_NOT_FOUND)
        if dairy_master not in []:
            company_rate = CompanyRate.objects.filter(mainId=request.query_params.get('id'))
            dairy_to_comapny_rate = DairyToCompanyMilk.objects.filter(mainId=request.query_params.get('id'))
            print("company_rate",company_rate)
            if company_rate not in []:
                company_rate.delete()
            if dairy_to_comapny_rate not in []:
                dairy_to_comapny_rate.delete()

            dairy_master.delete()
            return Response({'message':"success"},status=status.HTTP_200_OK)
        return Response({'message':"success"},status=status.HTTP_200_OK)


