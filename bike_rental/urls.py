from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (BikeViewSet, BikeRantalView,
                    CreateUserView, ReturnBikeView, UserRentalHistoryView)


router = DefaultRouter()
router.register(r'bikes', BikeViewSet)

urlpatterns = [
    # jwt api views
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # user registration urls
    path('register/', CreateUserView.as_view(), name='register'),

    # bike rental
    path('rent-bike/<int:bike_id>/', BikeRantalView.as_view(), name='rent-bike'),
    path('return-bike/<int:rental_id>/',
         ReturnBikeView.as_view(), name='return-bike'),

    # rental history
    path('rental-history/', UserRentalHistoryView.as_view(), name='rental-history'),

    path('', include(router.urls)),
]
