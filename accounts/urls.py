from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='registration'),
    path('auth/active/user/', VerifyCodeView.as_view(), name='verify_code'),
    path('auth/resend/code/', ResendCodeView.as_view(), name='resend_code'),
    path('auth/login/', TokenObtainPairView.as_view(), name='access_token'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('auth/verify_code/', VerifyCodeView.as_view(), name='verify_code'),
    path('auth/set_new_password/', SetNewPasswordView.as_view(), name='set_new_password'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    # for admin
    path('auth/users/', UserListView.as_view(), name='user_list'),
    path('auth/users/<int:pk>/', UserDetailsUpdateView.as_view(), name='user_details_update'),
    path('auth/users/activate/<int:id>/', UserActivateView.as_view(), name='user_activate'),
    path('auth/users/download/pdf/', download_all_user_view, name='download_all_users_pdf'),
    path('auth/users/download/excel/', download_all_user_excel_view, name='download_all_users_excel'),
]
