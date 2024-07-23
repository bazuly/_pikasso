from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions

from .views import (BikeViewSet, BikeRantalView,
                    CreateUserView, ReturnBikeView, UserRentalHistoryView)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = DefaultRouter()
router.register(r'bikes', BikeViewSet)

# drf-yasg schema_view settings 

schema_view = get_schema_view(
    openapi.Info(
        title="Bike Rental API",
        default_version='v1',
        description="API documentation for the Bike Rental application",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


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

    # swagger urls 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('', include(router.urls)),
]
