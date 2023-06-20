from django.contrib import admin
from .models import CarMake, CarModel

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car', 'dealer_id', 'car_type', 'year')

class CarModelInline(admin.TabularInline):
    model = CarModel

class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [CarModelInline]

admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
