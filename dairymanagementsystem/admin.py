from django.contrib import admin
from .models import Farm, LivestockType, CropType, Employee, Equipment, ProductionRecord, HealthSafetyRecord, EnvironmentalFactor, Activity, Document, Animal, Milk_product, Pregnancy, HeatObservation,Disease

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'owner_name', 'size_in_acres', 'revenue', 'expenses', 'profits')
    search_fields = ('name', 'location', 'owner_name')

@admin.register(LivestockType)
class LivestockTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(CropType)
class CropTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'farm')
    list_filter = ('farm',)
    search_fields = ('name',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'farm')
    list_filter = ('farm',)
    search_fields = ('name',)

@admin.register(ProductionRecord)
class ProductionRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'farm')
    list_filter = ('farm',)
    search_fields = ('farm__name',)

@admin.register(HealthSafetyRecord)
class HealthSafetyRecordAdmin(admin.ModelAdmin):
    list_display = ('description', 'farm')
    list_filter = ('farm',)
    search_fields = ('description', 'farm__name')

@admin.register(EnvironmentalFactor)
class EnvironmentalFactorAdmin(admin.ModelAdmin):
    list_display = ('description', 'farm')
    list_filter = ('farm',)
    search_fields = ('description', 'farm__name')

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'farm')
    list_filter = ('farm',)
    search_fields = ('name', 'farm__name')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'farm')
    list_filter = ('farm',)
    search_fields = ('name', 'farm__name')

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'breed', 'date_of_birth', 'gender', 'availability_status', 'pregnancy_status','get_cow_age')
    list_filter = ('breed', 'gender', 'availability_status', 'pregnancy_status')
    search_fields = ('name', 'breed__name')
    readonly_fields = ('get_cow_age',)

@admin.register(Milk_product)
class MilkProductAdmin(admin.ModelAdmin):
    list_display = ('milking_date', 'cow', 'milking_time_value', 'amount_in_kgs')
    search_fields = ('cow__name',)

@admin.register(Pregnancy)
class PregnancyAdmin(admin.ModelAdmin):
    list_display = ('cow', 'start_date', 'end_date', 'pregnancy_scan_date', 'notes')
    search_fields = ('cow__name',)
@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'occurrence_date', 'is_recovered', 'recovered_date', 'cows')
    list_filter = ('is_recovered', 'occurrence_date')
    search_fields = ('name', 'cows__name')
@admin.register(HeatObservation)
class HeatObservationAdmin(admin.ModelAdmin):
    list_display = ('cow', 'observation_date', 'notes')
    search_fields = ('cow__name',)
