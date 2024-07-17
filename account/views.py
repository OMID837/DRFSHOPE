from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from account.models import Account
from account.serializers import UserRegisterSerializers, UserLoginSerializers


class Register(APIView):
    def post(self, request):
        serializer = UserRegisterSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = request.build_absolute_uri(
            reverse('activate-account', kwargs={'uidb64': uid, 'token': token})
        )

        mail_subject = 'Activate your account'
        message = f"Hi {user.username},\n\nPlease click the link below to activate your account:\n{activation_link}\n\nThank you!"

        send_mail(mail_subject, message, 'your-email@gmail.com', [user.email])

        response_data = {
            'email': user.email,
            'username': user.username,
            'detail': 'Check your email for the activation link.'
        }

        return Response(data=response_data, status=status.HTTP_201_CREATED)


class ActivateAccountView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'detail': 'Account activated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Activation link is invalid!'}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        serializer = UserLoginSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = Account.objects.get(email=email)
            if user.check_password(password):
                data = {
                    'access_token': str(AccessToken.for_user(user)),
                    'refresh_token': str(RefreshToken.for_user(user)),
                }
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Account.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # return Response({'error': 'Unknown error'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)

            # Blacklist the refresh token
            token.blacklist()

            return Response({'message': 'شما با موفقیت خارج شدید'}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({'error': 'توکن بازآوری مورد نیاز است'}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # ساخت لینک ریست رمز عبور
        reset_link = request.build_absolute_uri(
            reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        )

        message = f"Hi {user.username},\n\nYou requested a password reset. Click the link below to reset your password:\n{reset_link}\n\nIf you did not request this, please ignore this email."
        mail_subject = 'Password Reset Request'
        send_mail(mail_subject, message, 'your-email@gmail.com', [user.email])

        return Response({'message': 'Password reset email has been sent'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            if not new_password:
                return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid token or user ID'}, status=status.HTTP_400_BAD_REQUEST)
