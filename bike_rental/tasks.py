from celery import shared_task
from django.utils import timezone
from .models import BikeRentalModel

@shared_task
def end_rental_and_calculate_cost(rental_id):
    try:
        rental = BikeRentalModel.objects.get(
            id=rental_id,
            rental_end__isnull=True
        )
        rental.rental_end = timezone.now()
        rental.save()
        rental.bike.status = 'available'
        rental.bike.save()

        rental_duration = rental.rental_end - rental.rental_start
        cost_per_hour = 10
        hours = rental_duration.total_seconds() / 3600
        cost = round(hours * cost_per_hour, 2)
        return cost
    except BikeRentalModel.DoesNotExist:
        return None
