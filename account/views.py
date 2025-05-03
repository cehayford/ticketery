from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import UserSerializer, Userinfoserializer, Bookinghistoryserializer
from rest_framework.response import Response
from rest_framework.status import *
from .models import UserInfo, BookingHistory
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from django.conf import settings


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist as e:
            return Response({"detail": str(e)+"Token not found."}, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        

class CreateUserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            users = UserInfo.objects.all()
            history = BookingHistory.objects.all()
            user_serializer = Userinfoserializer(users, many=True),
            history_serializer = Bookinghistoryserializer(history, many=True)
            comeback = {
                'users': user_serializer,
                'history': history_serializer
            }
            return Response(comeback.data)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            user_serializer = Userinfoserializer(data=request.data)
            history_serializer = Bookinghistoryserializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(user_serializer.errors, status=HTTP_400_BAD_REQUEST)

            if history_serializer.is_valid():
                history_serializer.save()
            else:
                return Response(history_serializer.errors, status=HTTP_400_BAD_REQUEST)
            comeback = {
                'users': user_serializer,
                'history': history_serializer
            }
            return Response(comeback.data, status=HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['PUT', 'PATCH'])
class UpdateUserInfoView(APIView):
    def put(self, request, pk):
        try:
            user = UserInfo.objects.get(userid = pk)
            history = BookingHistory.objecjs.get(historyid = pk)
            user_serializer = Userinfoserializer(user, data=request.data)
            history_serializer = Bookinghistoryserializer(history, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(user_serializer.errors, status=HTTP_400_BAD_REQUEST)

            if history_serializer.is_valid():
                history_serializer.save()
            else:
                return Response(history_serializer.errors, status=HTTP_400_BAD_REQUEST)
            comeback = {
                'user' : user_serializer,
                'history' : history_serializer
            }
            return Response(comeback.data, status=HTTP_202_ACCEPTED)
        except (UserInfo.DoesNotExist, BookingHistory.DoesNotExist) as e:
            return Response({'error': str(e)}, status= HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error':str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        try:
            user = UserInfo.objects.get(userid = pk)
            history = BookingHistory.objecjs.get(historyid = pk)
            user_serializer = Userinfoserializer(user, data=request.data)
            history_serializer = Bookinghistoryserializer(history, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(user_serializer.errors, status=HTTP_400_BAD_REQUEST)

            if history_serializer.is_valid():
                history_serializer.save()
            else:
                return Response(history_serializer.errors, status=HTTP_400_BAD_REQUEST)
            comeback = {
                'user' : user_serializer,
                'history' : history_serializer
            }
            return Response(comeback.data, status=HTTP_202_ACCEPTED)
        except (UserInfo.DoesNotExist, BookingHistory.DoesNotExist) as e:
            return Response({'error':str(e)}, status= HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error':str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        

# Watch it again and again
class sso_authentication(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                user = User.objects.get(email=email)
                token, _ = Token.objects.get_or_create(user=user)
                current_site = get_current_site(request)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                body = render_to_string('email_template.html', {
                    'email': user.email,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token.key,
                })
                subject = 'Activate your account'
                email_body = strip_tags(body)
                email_message = EmailMessage(subject, email_body, settings.EMAIL_HOST_USER, [user.email])
                email_message.send()
                return Response({"token": token.key, "message": "Email sent successfully"}, status=HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class sso_authentication_confirm(APIView):
    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                user.email = email
                user.save()
                if user.is_active:
                    return Response({"message": "User is authenticated"}, status=HTTP_200_OK)
                else:
                    return Response({"message": "User is not authenticated"}, status=HTTP_401_UNAUTHORIZED)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response({"error": "Token is invalid or expired"}, status=HTTP_400_BAD_REQUEST)
