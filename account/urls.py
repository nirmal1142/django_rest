from django.urls import path, include
from account.views import SendPasswordResetEmailView,ProductCreateView,ProductListView, UserLoginView, UserPasswordChangeView, UserPasswordResetView, UserProfileView, UserRegistrationView

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='user-registration'),
    path('login/',UserLoginView.as_view(),name='user-login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('changepassword/',UserPasswordChangeView.as_view(),name='changepassword'),
    path('send-reset-password-email/',SendPasswordResetEmailView.as_view(),name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name='reset-password'),
    path('product-list/',ProductListView.as_view(),name='product-list'),
    path('product-create', ProductCreateView.as_view(), name='product-create'),


]
