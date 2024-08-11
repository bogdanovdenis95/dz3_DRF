from django_filters import rest_framework as filters
from rest_framework import viewsets, status, generics
from .models import Payment
from .serializers import PaymentSerializer
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model

User = get_user_model()

class PaymentFilter(filters.FilterSet):
    course = filters.NumberFilter(field_name='course__id')
    lesson = filters.NumberFilter(field_name='lesson__id')
    payment_method = filters.ChoiceFilter(field_name='payment_method', choices=Payment.PAYMENT_METHOD_CHOICES)
    payment_date_gte = filters.DateTimeFilter(field_name='payment_date', lookup_expr='gte')
    payment_date_lte = filters.DateTimeFilter(field_name='payment_date', lookup_expr='lte')
    ordering = filters.OrderingFilter(fields=('payment_date',))

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method', 'payment_date_gte', 'payment_date_lte']

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PaymentFilter


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]
