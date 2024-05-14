from django import forms
from .models import Farm

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'location', 'owner_name', 'owner_contact', 'owner_address', 
                  'size_in_acre', 'farm_type', 'barns', 'sheds', 'irrigation_system', 
                  'revenue', 'expenses', 'profits']
