from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Contact
from .serializers import ContactSerializer

# Create your views here.

class ContactViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin ,viewsets.GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return super(ContactViewSet, self).get_permissions()