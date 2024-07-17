from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='Login'),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate-account'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]

# {
#     "username":
#         "oooo"
#     ,
#     "password":
#         "oooo"
#     ,
#     "confirm_password":
#         "oooo"
#     ,
#    "email":
#         " feaa998423@emailcbox.pro "
# }
#
# {
#     "password":
#         "omid1"
#     ,
#    "email":
#         "2e08e0881b@emailcbox.pro"
# }