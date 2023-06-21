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

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:
    def __init__(self, dealership, name, purchase, sentiment, review, id, car_make, car_model, car_year):
        self.dealership = dealership
        self.name = name 
        self.purchase = purchase
        self.review = review
        self.car_make = car_make
        self.car_year = car_year
        self.car_model = car_model
        self.sentiment = sentiment
        self.id = id
