from django import forms
from .models import Milk_product,Farm,Animal

class MilkForm(forms.ModelForm):
    class Meta:
        model = Milk_product
        fields = ['amount_in_kgs']  # Exclude milking_time_value field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount_in_kgs'].widget.attrs['min'] = 0  # Set minimum value for amount_in_kgs fie


class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'location', 'owner_name', 'owner_contact', 'owner_address', 
                  'size_in_acres', 'farm_type', 'barns', 'sheds', 'irrigation_system', 
                  'revenue', 'expenses', 'profits']
        
class FarmSearchForm(forms.Form):
    farm_name = forms.CharField(label='Farm Name', max_length=100)


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = '__all__'
        exclude = ['id']


class MilkForm(forms.ModelForm):
    class Meta:
        model = Milk_product
        fields = '__all__'        


