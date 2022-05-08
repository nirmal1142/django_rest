from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,renderer_classes
from rest_framework.views import APIView
from rest_framework import status
from account.serializers import ProductUpdateSerializer, ProductGetByCategorySerializer, CategoryCreateSerializer, ProductDetailSerializer,CategorySerializer,ProductCreateSerializer, UserPasswordChangeSerializer, UserPasswordResetSerializer, UserRegistrationSerializer ,UserLoginSerializer , UserProfileSerializer , SendPasswordResetEmailSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRender
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from account.models import Products,Category,User
import io
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse


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
                user_data = UserProfileSerializer(user).data
                return Response({'token':token,'msg':'Login successfully','user_data':user_data },status=status.HTTP_200_OK)
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([UserRender])
def get_user_list(request):
    users = User.objects.all()
    serializer = UserProfileSerializer(users,many=True)
    count  = len(serializer.data)
    data = {
        'users':serializer.data,
        'count':count
    }
    return Response(data,status=status.HTTP_200_OK)


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
        products = ProductDetailSerializer(products, many=True)
        if products:
            return Response(products.data,status=status.HTTP_200_OK)
        return Response({'msg':'No products found'},status=status.HTTP_404_NOT_FOUND)

class ProductCreateView(APIView):
    renderer_clssses = [UserRender]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = ProductCreateSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = serializer.data
            return Response({'msg':'Product created successfully', 'data':  data},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class ProductGetByCategoryView(APIView):
    renderer_clssses = [UserRender]
    permission_classes = [IsAuthenticated]
    def get(self,request,category,format=None):
        products = Products.objects.filter(category=category)
        products = ProductDetailSerializer(products, many=True)
        if products:
            return Response(products.data,status=status.HTTP_200_OK)
        return Response({'msg':'No products found'},status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@renderer_classes([UserRender])
def product_is_active(request,id):
    product = Products.objects.get(id=id)
    if product.is_active:
        product.is_active = False
    else:
        product.is_active = True
    product.save()
    return Response({'msg':'Product is active status changed successfully'},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([UserRender])
def get_product_by_category(request,category):
    products = Products.objects.filter(category=category)
    products = ProductDetailSerializer(products, many=True)
    if products:
        return Response(products.data,status=status.HTTP_200_OK)
    return Response({'msg':'No products found'},status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE','PUT'])
@permission_classes([IsAuthenticated])
@renderer_classes([UserRender])
def product_detail(request,id):
    if request.method == 'DELETE':
        try:
            product = Products.objects.get(id=id)
        except Products.DoesNotExist:
            return Response({'msg':'Product not found'},status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({'msg':'Product deleted successfully'},status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        try:
            product = Products.objects.get(id=id)
        except Products.DoesNotExist:
            return Response({'msg':'Product not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ProductUpdateSerializer(product,data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = serializer.data
            return Response({'msg':'Product updated successfully', 'data':  data},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([UserRender])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        categories = CategorySerializer(categories, many=True)
        if categories:
            return Response(categories.data,status=status.HTTP_200_OK)
        return Response({'msg':'No categories found'},status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        user = request.user
        print("user----",user)
        serializer = CategoryCreateSerializer(data=request.data)
        print("serializer----",serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = serializer.data
            return Response({'msg':'Category created successfully', 'data':  data},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE','PUT'])
@permission_classes([IsAuthenticated])
@renderer_classes([UserRender])
def category_delete(request,pk):
    if request.method == 'DELETE':
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'msg':'Category does not exist'},status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response({'msg':'Category deleted successfully'},status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'msg':'Category does not exist'},status=status.HTTP_404_NOT_FOUND)
        serializer = CategoryCreateSerializer(category,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = serializer.data
            return Response({'msg':'Category updated successfully', 'data':  data},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






