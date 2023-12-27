from rest_framework import serializers
from django.contrib.auth.models import User as Account
from django.contrib.auth.tokens import default_token_generator
from  django.core.mail import send_mail
from django.template.loader import render_to_string
import django.contrib.auth.password_validation as validators
from django.conf import settings
from .models import AccountRequest


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        exclude = ['password',]

class CreateAccountSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)

    def save(self, **kwargs):
        #TODO: Create a proper message for the email
        #TODO: Do proper error handling
        account = super().save(**kwargs)
        token = default_token_generator.make_token(account)
        #Sending the email
        html_message = render_to_string('welcome_email.html', {'link': settings.USER_FRONTEND_DOMAIN + '/' + token + '/' + str(account.id)})
        send_mail('Welcome!', None , None, (account.email,),  html_message=html_message)
        return account

    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name']

class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, write_only=True, validators=[validators.validate_password])
    token = serializers.CharField(write_only=True)

    def validate_token(self, value):
        if not default_token_generator.check_token(self.instance, value):
            raise serializers.ValidationError({'token': 'Token is not valid'})
        return value
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class AccountRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountRequest
        fields = '__all__'