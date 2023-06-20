from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    OPTIONS = [('SD', 'Sedan'), ('SV', 'SUV'), ('WG', 'Wagon')]
    car = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    dealer_id = models.IntegerField()
    car_type = models.CharField(max_length=30, choices=OPTIONS)
    year = models.DateField()

    def __str__(self):  
        return self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
