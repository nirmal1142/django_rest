from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from account.serializers import ProductDetailSerializer,ProductCreateSerializer, UserPasswordChangeSerializer, UserPasswordResetSerializer, UserRegistrationSerializer ,UserLoginSerializer,ProductSerializer , UserProfileSerializer , SendPasswordResetEmailSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRender
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from account.models import Products


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_clssses = [UserRender]
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
           user = serializer.save()
           token = get_token_for_user(user)
           return Response({'token':token,'msg':'Registation successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_clssses = [UserRender]
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request,email=email,password=password)
            if user is not None:
                token = get_token_for_user(user)
                return Response({'token':token,'msg':'Login successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Invalid credentials']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class UserProfileView(APIView):
    renderer_clssses = [UserRender]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None): 
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)


class UserPasswordChangeView(APIView):
    renderer_clssses = [UserRender]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        user = request.user
        serializer = UserPasswordChangeSerializer(data=request.data,context={'user':user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password changed successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):
    renderer_clssses = [UserRender]
    def post(self,request,format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset email sent successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):
    renderer_clssses = [UserRender]
    def post(self,request,uid,token,format=None):
        serializer = UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password changed successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ProductListView(APIView):
    renderer_clssses = [UserRender]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):

        products = Products.objects.all()
        # products = request.user.products.all()
        products = ProductDetailSerializer(products, many=True)
        print("products----------",products)
        if products:
            return Response(products.data,status=status.HTTP_200_OK)
        return Response({'msg':'No products found'},status=status.HTTP_404_NOT_FOUND)

        # serializer = ProductDetailSerializer(products,many=True)
        # return Response(serializer.data,status=status.HTTP_200_OK)


class ProductCreateView(APIView):
    renderer_clssses = [UserRender]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = ProductCreateSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':'Product created successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


