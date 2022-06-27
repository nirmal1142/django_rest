from django.shortcuts import render
from django.http import HttpResponse
from dairymaster.serializers import DairyMasterGetSerializer,DairyMasterSerializer ,CompanyProfileSerializer,DairyMasterUpdateSerializer,DairyToCompanyMilkSerializer,CompanyRateSerializer
from rest_framework.decorators import api_view  ,renderer_classes , permission_classes
from rest_framework import status
from dairymaster.renderers import UserRender
from rest_framework.response import Response
from rest_framework.views import APIView
from dairymaster.models import DairyMaster ,CompanyProfile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
import json
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from account.models import User
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)



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
        # dairy_master = DairyMaster.objects.filter(user=user)
        # print("dairy_master+++++",dairy_master)
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

        user = User.objects.get(id=request.user.id)

        # print("user+++",user.id)
        # user_id = json.dumps({'user':user.id})

        # user_id = json.dumps(user, cls=UUIDEncoder)

        print("user_id",request.user)

        data = request.data
        data['user'] = request.user.id
        print(data)
        searializer = DairyMasterSerializer(data=data)
        # print(searializer)

        if searializer.is_valid(raise_exception=True):
            searializer.save()
            data = {
                'message': 'Daily Milk Details Added Successfully',
                'status': 'success',
                'data': searializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(searializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DairyMasterUpdateView(APIView):
    def put(self, request, pk, format=None):
        dairy_master = DairyMaster.objects.get(pk=pk)
        serializer = DairyMasterUpdateSerializer(dairy_master, data=request.data)
        print(serializer)

        # print("serializer",serializer)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message': 'Daily Milk Details Updated Successfully',
                'status': 'success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['GET', 'PUT', 'DELETE'])
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

    if request.method == 'GET':
        serializer = DairyMasterSerializer(dairy_master, many=True)

        if serializer:
            data ={
                'status':'success',
                'data':serializer.data,
                'count':len(serializer.data)
            }
            return Response(data , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        dairy_master = DairyMaster.objects.get(id=request.query_params.get('id'))
        dairy_master.delete()
        data = {
            'message': 'Daily Milk Details Deleted Successfully',
            'status': 'success'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)





@api_view(['POST'])
@renderer_classes([UserRender])
def daily_milk_details_get_by_many_date(request, format=None):

    try :
        if request.data:
            dairy_master = DairyMaster.objects.filter(date__in=request.data)
        else:
            dairy_master = DairyMaster.objects.all()
    except DairyMaster.DoesNotExist:
        return Response({'message':'not found'},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = DairyMasterSerializer(dairy_master, many=True)
        print(serializer)
        if serializer.data:
            data ={
                'status':'success',
                'data':serializer.data,
                'count':len(serializer.data)
            }
            return Response(data , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET','POST'])
@renderer_classes([UserRender])
def company_profile(request , format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = CompanyProfile.objects.all()
        serializer = CompanyProfileSerializer(snippets, many=True)
        print(serializer.data)
        if serializer.data:
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        searializer = CompanyProfileSerializer(data=request.data)
        if searializer.is_valid(raise_exception=True):
            searializer.save()
            return Response(searializer.data, status=status.HTTP_201_CREATED)
        return Response(searializer.errors, status=status.HTTP_400_BAD_REQUEST)