import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import BikeModel, BikeRentalModel

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def bike():
    return BikeModel.objects.create(name='X5', bike_type='urban', status='available')

@pytest.fixture
def rented_bike(user, bike):
    rental = BikeRentalModel.objects.create(user=user, bike=bike)
    bike.status = 'unavailable'
    bike.save()
    return rental

@pytest.mark.django_db
def test_user_registration(api_client):
    response = api_client.post('/register/', {'username': 'newuser', 'password': 'newpass'})
    assert response.status_code == 201
    assert User.objects.filter(username='newuser').exists()

@pytest.mark.django_db
def test_bike_rental(api_client, user, bike):
    api_client.force_authenticate(user=user)
    response = api_client.post(f'/rent-bike/{bike.id}/')
    assert response.status_code == 201
    bike.refresh_from_db()
    assert bike.status == 'unavailable'
    assert BikeRentalModel.objects.filter(user=user, bike=bike).exists()

@pytest.mark.django_db
def test_bike_return(api_client, user, rented_bike):
    api_client.force_authenticate(user=user)
    response = api_client.post(f'/return-bike/{rented_bike.id}/')
    assert response.status_code == 200
    rented_bike.refresh_from_db()
    assert rented_bike.rental_end is not None
    rented_bike.bike.refresh_from_db()
    assert rented_bike.bike.status == 'available'

@pytest.mark.django_db
def test_rental_history(api_client, user, rented_bike):
    api_client.force_authenticate(user=user)
    response = api_client.get('/rental-history/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == rented_bike.id
