import uuid
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)
from api.serializers import (CreateUserSerializer, LoginUserSerializer,
                             UserSerializer, MeUserSerializer)
from users.models import User
from django.core.mail import send_mail
from api.permissions import AdminOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from api_yamdb.settings import EMAIL_HOST_USER


class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny, ]

    def generate_code(self):
        return str(uuid.uuid4())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers)

    def perform_create(self, serializer):
        code = self.generate_code()
        user_email = serializer.validated_data['email']
        serializer.save(confirmation_code=code)
        send_mail(
            subject='Код авторизации для yamdb',
            message=f'Ваш код авторизации: {code}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=False,
        )


class ObtainTokenView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if data['confirmation_code'] == user.confirmation_code:
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }, status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    permission_classes = (AdminOnly,)

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def me_actions(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == "GET":
            serializer = MeUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "PATCH":
            serializer = MeUserSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
