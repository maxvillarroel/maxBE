from django.conf import settings
from django.contrib.auth.models import User as Account, update_last_login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status, viewsets, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated 
from maxBE.permissions import ReadOnly
from .models import AccountRequest
from .permissions import IsSelf, SafeFieldsOnly
from rest_framework.response import Response
from .serializers import AccountSerializer, CreateAccountSerializer, SetPasswordSerializer, AccountRequestSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAdminUser]

    def create(self, request):
        """
        It creates a new user with a random password and a token for it. It then sends it by email to the user.
        """
        serializer = CreateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save(password=Account.objects.make_random_password())
        return Response(self.serializer_class(account).data)

    @action(detail=True, methods=['post'], permission_classes = [AllowAny])
    def set_password(self, request, pk=None):
        """
        It validates the password and then check token, then sets the new password for the user. 
        """
        account = self.get_object()
        serializer = SetPasswordSerializer(account, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Your password has been successfully saved'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes = [AllowAny])
    def login(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=account)
        update_last_login(None, account)
        return Response({'token': token.key, 'account': self.serializer_class(account).data})

    @action(detail=True, methods=['get'], permission_classes = [IsAdminUser | IsSelf])
    def reset_password(self, request, pk=None):
        account = self.get_object()
        account.set_password(Account.objects.make_random_password())
        account.save()
        token = default_token_generator.make_token(account)
        html_message = render_to_string('reset_email.html', {'link': settings.USER_FRONTEND_DOMAIN + token + '/' + str(account.id)})
        account.email_user('Password Reset', None, html_message=html_message)

        return Response({'message': 'The user has been sent an email to reset password'}, status=status.HTTP_200_OK)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            self.permission_classes = [IsAdminUser | (IsAuthenticated & ReadOnly)]
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated]
        if self.action =='destroy':
            self.permission_classes = [IsAdminUser | IsSelf]
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAdminUser | IsSelf, SafeFieldsOnly]
        return super(AccountViewSet, self).get_permissions()
    
class AccountRequestViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin ,viewsets.GenericViewSet):
    queryset = AccountRequest.objects.all()
    serializer_class = AccountRequestSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return super(AccountRequestViewSet, self).get_permissions()