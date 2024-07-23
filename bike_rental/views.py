from rest_framework import generics, viewsets
from rest_framework import permissions, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from bike_rental.tasks import end_rental_and_calculate_cost

from .serializers import (UserSerializer, BikeSerializer, RentalSerializer,
                          RentalReturnSerializer, BikeRentalHistorySerializer)
from .models import BikeModel, BikeRentalModel

""" 
Регистрация пользователя 
"""


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    model = User
    permission_classes = (
        permissions.AllowAny,
    )
    serializer_class = UserSerializer


""" 
Получение всех доступных велосипедов
"""


class BikeViewSet(viewsets.ModelViewSet):
    queryset = BikeModel.objects.all()
    serializer_class = BikeSerializer
    permission_classes = [permissions.IsAuthenticated, ]


""" 
Аренда велосипедов
"""


class BikeRantalView(APIView):
    def post(self, request, bike_id):
        user = request.user

        active_rental = BikeRentalModel.objects.filter(
            user=user,
            rental_end__isnull=True,
        ).first()
        if active_rental:
            return Response(
                {'error': 'У вас уже есть арендованный велосипед'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            bike = BikeModel.objects.get(id=bike_id)
        except BikeModel.DoesNotExist:
            return Response(
                {'error': 'Велосипел не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if bike.status != 'available':
            return Response(
                {'error': 'Велосипед уже арнедован'},
                status=status.HTTP_400_BAD_REQUEST
            )
        rental = BikeRentalModel.objects.create(user=user, bike=bike)
        bike.status = 'unavailable'
        bike.save()

        serializer = RentalSerializer(rental)   
        return Response(serializer.data, status=status.HTTP_201_CREATED)


""" 
Завершение аренды велосипедов
"""


class ReturnBikeView(APIView):
    def post(self, request, rental_id):
        try:
            rental = BikeRentalModel.objects.get(
                id=rental_id,
                user=request.user,
                rental_end__isnull=True
        )
        except BikeRentalModel.DoesNotExist:
            return Response(
                {'error': 'Аренда отсутствует или уже завершена'},
                status=status.HTTP_400_BAD_REQUEST
        )
        
        # Запуск задачи Celery для завершения аренды и расчета стоимости
        task = end_rental_and_calculate_cost.delay(rental.id)
        
        cost = task.get()

        if cost is None:
            return Response(
                {'error': 'Ошибка при завершении аренды'},
                status=status.HTTP_400_BAD_REQUEST
        )

        rental.refresh_from_db()
        serializer = RentalReturnSerializer(rental)
        return Response(
            {'rental': serializer.data, 'cost': cost},
            status=status.HTTP_200_OK
        )


""" 
История аренды пользователя
"""


class UserRentalHistoryView(generics.ListAPIView):
    serializer_class = BikeRentalHistorySerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return BikeRentalModel.objects.filter(user=self.request.user)

