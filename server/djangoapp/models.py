from django.db import models
from django.utils.timezone import now

# Define the model that contains the car maker info
class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    
# Define the model that contains the car model info
class CarModel(models.Model):
    CAR_TYPES = (
        ('1', 'Sedan'),
        ('2', 'SUV'),
        ('3', 'Hatch'),
        ('4', 'Other'),
    )
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    dealer_id = models.IntegerField()
    car_type =  models.CharField(max_length=1, choices=CAR_TYPES)
    year = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name + self.year

# Create a class to hold dealer data (get from icloudant)
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer data
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name
    
# Create a class to hold the dealer review data (get from icloudant)
class DealerReview:
    
    def __init__(self, id, name, dealership, review, purchase, sentiment, **kwargs):
        # Review data
        self.id = id
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.sentiment = sentiment
        
        # If it has a purchase, populate other fields
        if purchase:
            self.purchase_date = kwargs["purchase_date"]
            self.car_make = kwargs["car_make"]
            self.car_model = kwargs["car_model"]
            self.car_year = kwargs["car_year"]
    
    def __str__(self):
        return "Review: " + self.review