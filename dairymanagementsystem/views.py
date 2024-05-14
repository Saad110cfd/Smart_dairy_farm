from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound,HttpResponse
from django.contrib import messages
from django.db import OperationalError,IntegrityError
from .models import Farm, Animal,Milk_product
from .forms import FarmForm, FarmSearchForm, AnimalForm, MilkForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    return render(request, 'users/index.html')

def farm_detail(request):
    if request.method == 'GET':
        form = FarmSearchForm()
        return render(request, 'farm_detail_input.html', {'form': form})
    elif request.method == 'POST':
        form = FarmSearchForm(request.POST)
        if form.is_valid():
            farm_name = form.cleaned_data.get('farm_name')
            try:
                farm = Farm.objects.get(name=farm_name)
                return render(request, 'farm_detail.html', {'farm': farm})
            except Farm.DoesNotExist:
                return HttpResponseNotFound('<h1>Farm not found</h1>')
        else:
            return render(request, 'farm_detail_input.html', {'form': form})

def add_farm(request):
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = form.save()
            messages.success(request, f"Farm added successfully with ID: {farm.id}")
            return redirect('users:index')
    else:
        form = FarmForm()
    return render(request, 'dairyfarm/add_farm.html', {'form': form})

def edit_farm(request):
    if request.method == 'POST':
        farm_name = request.POST.get('farm_name')
        try:
            farm = Farm.objects.get(name=farm_name)
            return redirect('users:edit_farm_detail', farm_id=farm.id)
        except Farm.DoesNotExist:
            messages.error(request, f"Farm with name '{farm_name}' does not exist.")
            return redirect('edit_farm')
    return render(request, 'edit_farm_search.html')

def edit_farm_detail(request, farm_id):
    farm = get_object_or_404(Farm, pk=farm_id)
    if request.method == 'POST':
        form = FarmForm(request.POST, instance=farm)
        if form.is_valid():
            form.save()
            messages.success(request, f"Farm details updated successfully for Farm ID: {farm_id}")
            return redirect('users:index')
    else:
        form = FarmForm(instance=farm)
    farm_string_representation = farm.get_string_representation()
    return render(request, 'dairyfarm/edit_farm.html', {'form': form, 'farm_id': farm_id, 'farm_string_representation': farm_string_representation})

def delete_farm(request):
    if request.method == 'POST':
        try:
            farm_name = request.POST.get('farm_name')
            farm = get_object_or_404(Farm, name=farm_name)
            farm_name = farm.name
            farm.delete()
            messages.success(request, f"Farm '{farm_name}' deleted successfully.")
        except OperationalError as e:
            messages.error(request, "An error occurred while deleting the farm. Please try again later.")
        except Farm.DoesNotExist:
            messages.error(request, f"Farm with name '{farm_name}' does not exist.")
        return redirect('users:index')
    else:
        return render(request, 'delete_farm.html')

def animal_add(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            # Save the form data to create a new Animal instance
            form.save()
            return redirect('users:index')  # Redirect to animal list view after successful addition
    else:
        form = AnimalForm()

    return render(request, 'animal_add.html', {'form': form}) 
def animal_details(request):
    error_message = None

    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            animal_name = form.cleaned_data.get('animal_name')
            animal = get_object_or_404(Animal, name=animal_name)
            return render(request, 'animal_detail.html', {'animal': animal})
        else:
            print(form.errors)  # Print form errors for debugging
            error_message = 'Invalid form input'
    else:
        form = AnimalForm()

    return render(request, 'animal_detail_search.html', {'form': form, 'error_message': error_message})
def edit_animal(request):
    if request.method == 'POST':
        animal_name = request.POST.get('animal_name')
        print("Animal name:", animal_name)  # Add this line for debugging
        try:
            animal = Animal.objects.get(name=animal_name)
            return redirect('users:edit_animal_details', animal_name=animal_name)
        except Animal.DoesNotExist:
            print("Animal does not exist")  # Add this line for debugging
            messages.error(request, f"Animal with name '{animal_name}' does not exist.")
            return redirect('edit_animal')  # Redirect back to the edit_animal page
    return render(request, 'edit_animal_search.html')

def edit_animal_details(request, animal_name):
    animal = get_object_or_404(Animal, name=animal_name)
    if request.method == 'POST':
        form = AnimalForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, f"Animal details updated successfully for '{animal_name}'")
            return redirect('users:index')
    else:
        form = AnimalForm(instance=animal)
    return render(request, 'edit_animal_details.html', {'form': form, 'animal': animal})


def delete_animal(request):
    if request.method == 'POST':
        try:
            animal_name = request.POST.get('animal_name')
            print("Animal Name:", animal_name)  # Debugging statement
            animal = get_object_or_404(Animal, name=animal_name)
            animal.delete()
            messages.success(request, f"Animal '{animal_name}' deleted successfully.")
        except IntegrityError as e:
            messages.error(request, "An error occurred while deleting the Animal. Please try again later.")
        except Animal.DoesNotExist:
            messages.error(request, f"Animal with name '{animal_name}' does not exist.")
        return redirect('users:index')
    else:
        return render(request, 'delete_animal.html')
    


def add_milk_production(request):
    if request.method == "POST":
        form = MilkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:index')
    else:
        form = MilkForm()
    return render(request, 'dairyfarm/milk.html', {'form': form})


from django.db.models import Q

def milk_detail(request):
    if request.method == 'POST':
        animal_name = request.POST.get('animal_name')
        if animal_name:
            try:
                animal = Animal.objects.get(name=animal_name)
                milk_production = Milk_product.objects.filter(Q(cow__name=animal_name))
                return render(request, 'milk_detail.html', {'animal': animal, 'milk_production': milk_production})
            except Animal.DoesNotExist:
                messages.error(request, f"Animal with name '{animal_name}' does not exist.")
        else:
            messages.error(request, "Please provide an animal name.")
    return render(request, 'milk_detail.html')



