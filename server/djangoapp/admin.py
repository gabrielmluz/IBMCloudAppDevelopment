from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

class CarModelAdmin(admin.ModelAdmin):
    fields = ['carmake', 'name', 'dealer_id', 'car_type', 'year']

class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    inlines = [CarModelInline]

admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)