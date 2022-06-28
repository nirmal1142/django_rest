from rest_framework import serializers
from account.models import User, Products, Category
from django.utils.encoding import smart_str , force_bytes , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email','name','tc','password','password2'] 
        extra_kwargs = {'password':{'write_only':True}}
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError('Passwords must match')
        return attrs


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,min_length=3)
    class Meta:
        model = User
        fields = ['email','password']
        extra_kwargs = {'password':{'write_only':True}}


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name','tc','is_admin','is_active']


class UserPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style = {'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style = {'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Passwords must match')
        user.set_password(password)
        user.save()
        return attrs 

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print("user",user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            print("token:",token)
            link = 'http://localhost:8000/api/user/reset/'+uid+'/'+token
            data = {
                'subject':'Password Reset',
                'body':'Click on the link to reset your password: '+link,
                'to':user.email
            }
            Util.send_email(data)
            print("mail link",link)
            return attrs
        else:
            raise serializers.ValidationError('Email not found')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style = {'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style = {'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']
        
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError('Passwords must match')
            id = smart_str(urlsafe_base64_decode(uid))
            print("id",id)
            user = User.objects.get(id=id)
            print("user",user)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError('Token is invalid')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError('Token is invalid')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {'created_at': {'read_only': True}}


class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = ['id','name','price','description','image','category','created_at','updated_at','is_active','user_id']
        depth = 1

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id','name','price','description','image','category','user']
        # extra_kwargs = {
        #     'user': {'read_only': True}
        # }

class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id','name','price','description','image','category']
        extra_kwargs = {
            'user': {'read_only': True}
        }

class ProductGetByCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id','name','price','description','image','category']
        depth = 1
