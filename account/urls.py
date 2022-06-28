from django.urls import path, include, re_path
from account.views import get_user_list,get_product_by_category,product_is_active, product_detail,ProductGetByCategoryView,  category_list,category_delete, SendPasswordResetEmailView,ProductCreateView,ProductListView, UserLoginView, UserPasswordChangeView, UserPasswordResetView, UserProfileView, UserRegistrationView
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer


urlpatterns = [

    path('register/',UserRegistrationView.as_view(),name='user-registration'),
    path('login/',UserLoginView.as_view(),name='user-login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('changepassword/',UserPasswordChangeView.as_view(),name='changepassword'),
    path('send-reset-password-email/',SendPasswordResetEmailView.as_view(),name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name='reset-password'),

    path('get-user-list/',get_user_list,name='get-user-list'),

    path('category-list/', category_list, name='category-list'),
    path('category-delete/<pk>/', category_delete, name='category-delete'),
    path('category-update/<pk>/', category_delete, name='category-update'),

    path('product-create', ProductCreateView.as_view(), name='product-create'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('product-delete/<id>/', product_detail, name='product-delete'),
    path('product-update/<id>/', product_detail, name='product-update'),
    path('product-get-by-category/<category>/', get_product_by_category, name='product-get-by-category'),
    path('product-is-active/<id>/', product_is_active, name='product-is-active'),


]
