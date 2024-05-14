from django.db import models
# Create your models here.
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
import datetime
from datetime import timedelta,date
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class Farm(models.Model):
    
    name = models.CharField(max_length=32, blank=True, null=True)
    location = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=100, blank=True, null=True)
    owner_contact = models.CharField(max_length=20, blank=True, null=True)
    owner_address = models.TextField(blank=True, null=True)
    size_in_acres = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    farm_type = models.CharField(max_length=50, blank=True, null=True)
    barns = models.PositiveIntegerField(default=0)
    sheds = models.PositiveIntegerField(default=0)
    irrigation_system = models.BooleanField(default=False)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    expenses = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    profits = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Farm"
    def get_string_representation(self):
        return f"ID: {self.id}, Name: {self.name}, Location: {self.location}, Owner: {self.owner_name}"
    @staticmethod
    def get_farm_by_name(name):
        """
        Retrieve a farm by its name.
        """
        return get_object_or_404(Farm, name=name)
class LivestockType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CropType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='employees')

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='equipment')

    def __str__(self):
        return self.name

class ProductionRecord(models.Model):
    date = models.DateField()
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='production_records')

    def __str__(self):
        return f"Production Record for {self.farm.name} on {self.date}"

class HealthSafetyRecord(models.Model):
    description = models.TextField()
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='health_safety_records')

    def __str__(self):
        return f"Health and Safety Record for {self.farm.name}"

class EnvironmentalFactor(models.Model):
    description = models.TextField()
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='environmental_factors')

    def __str__(self):
        return f"Environmental Factor for {self.farm.name}"

class Activity(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='activities')

    def __str__(self):
        return self.name

class Document(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return self.name

from django.db import models

from django.db import models, IntegrityError

class Animal(models.Model):
    STATUS_CHOICES = [
        ('A', 'Alive'),
        ('D', 'Dead'),
        ('S', 'Sold')
    ]
    PREGNANCY_STATUS = [
        ('P', 'Pregnant'),
        ('C', 'Calved'),
        ('N', 'Not pregnant')
    ]
    name = models.CharField(max_length=32, blank=True, null=True)
    breed = models.CharField(max_length=32)  # Change this to CharField
    date_of_birth = models.DateField(validators=[MaxValueValidator(datetime.date.today)], error_messages={'max_value': 'The date of birth cannot be in the future'})
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), db_index=True)
    availability_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    pregnancy_status = models.CharField(max_length=1, choices=PREGNANCY_STATUS, default='N')
    date_of_death = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else f"Cow {self.id}"

    def get_cow_age(self):
        # Calculate age based on the date_of_birth of the cow
        today = datetime.date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age
class Pregnancy(models.Model):
    cow = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='pregnancies')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    pregnancy_scan_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be before the start date of pregnancy.")
        if self.start_date > datetime.date.today():
            raise ValidationError("Start date of pregnancy cannot be in the future.")
        if self.end_date and self.end_date > datetime.date.today():
            raise ValidationError("End date of pregnancy cannot be in the future.")
        if self.pregnancy_scan_date and self.pregnancy_scan_date > datetime.date.today():
            raise ValidationError("Pregnancy scan date cannot be in the future.")

    def __str__(self):
        return f"Pregnancy of cow {self.cow.name}"


class HeatObservation(models.Model):
    cow = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='heat_observations')
    observation_date = models.DateField()
    notes = models.TextField(blank=True)

    def clean(self):
        if self.observation_date > datetime.date.today():
            raise ValidationError("Observation date cannot be in the future.")

    def __str__(self):
        return f"Heat observation of cow {self.cow.name} on {self.observation_date}"
 
class Milk_product(models.Model):
    MILKING_TIMES = [
        (1, "Morning"),
        (2, "Afternoon"),
        (3, "Evening"),
        (4, "Night")
    ]

    milking_time_value = models.IntegerField(choices=MILKING_TIMES)
    milking_date = models.DateTimeField(auto_now_add=True)
    cow = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='milk')
    amount_in_kgs = models.DecimalField(verbose_name="Amount (kg)", default=0.00, max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0, message="Amount of milk cannot be less than 0 kgs")])

    class Meta:
        verbose_name_plural = "Milk"
        unique_together = ('cow', 'milking_time_value')

    def __str__(self):
        return f"Milk record of cow {self.cow.name} at {self.get_milking_time_value_display()} on {self.milking_date.strftime('%Y-%m-%d %H:%M:%S')}"

    def clean(self):
        if self.cow.availability_status == "D":
            raise ValidationError("Cannot add milk record for a dead cow.")
        if self.cow.availability_status == "S":
            raise ValidationError("Cannot add milk record for a sold cow.")
        if self.cow.get_cow_age() < 1.75:
            raise ValidationError('Cow is less than 21 months old and should not have a milk record')
        if not self.milking_time_value:
            raise ValidationError("Milking time value must be specified.")
        if not self.milking_date:
            self.milking_date = timezone.now()
        if self.amount_in_kgs is not None and self.amount_in_kgs <= 0:
            raise ValidationError("Amount in kgs should be greater than 0")
        try:
            existing_milk_record = Milk_product.objects.get(
                cow=self.cow,
                milking_date__date=self.milking_date.date(),
                milking_time_value=self.milking_time_value
            )
            if existing_milk_record and not self.pk:
                raise ValidationError("A milk record already exists for this cow at this milking time")
        except Milk_product.DoesNotExist:
            pass
        if self.cow.gender != "F":
            raise ValidationError("This cow is not female and cannot produce milk")
        
class Disease(models.Model):
    name = models.CharField(max_length=50, unique=True)
    occurrence_date = models.DateField()
    is_recovered = models.BooleanField(default=False)
    recovered_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    cows = models.ForeignKey(Animal, related_name="diseases", on_delete=models.CASCADE)
    symptoms = models.TextField(blank=True)
    treatment = models.TextField(blank=True)

    class Meta:
        verbose_name = "Disease \U0001F48A"
        verbose_name_plural = "Diseases \U0001F48A"

    def __str__(self):
        return "{} ({}) occurred on {}".format(self.name, self.occurrence_date, self.cows)

    def clean(self):
        if self.is_recovered and not self.recovered_date:
            raise ValidationError("Recovered date is required if the disease is marked as recovered")
        if self.recovered_date and not self.is_recovered:
            raise ValidationError("Recovered date is required when the animal is recovered")
        if not self.name:
            raise ValidationError("Name is necessary")
        if self.occurrence_date > timezone.now().date():
            raise ValidationError("Occurrence cannot be in the future")
        if self.recovered_date and self.occurrence_date > self.recovered_date:
            raise ValidationError("Recovered date must be after the occurrence date")