from django.contrib import admin
from .models import CarMake, CarModel

# Stacked info for control in admin panel (CarMake + CarMake)
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

# CarModel admin model (fields on admin panel)
class CarModelAdmin(admin.ModelAdmin):
    fields = ['carmake', 'name', 'dealer_id', 'car_type', 'year']

# CarMake admin model (fields on admin panel)
# Related with CarModel with one to many relationship
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    inlines = [CarModelInline]

# Register models in the admin panel
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)