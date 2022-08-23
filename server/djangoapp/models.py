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

# <HINT> Create a plain Python class `DealerReview` to hold review data
