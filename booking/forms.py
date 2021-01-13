from django import forms
from .models import Client


class NewClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields =  '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),  
            'barber': forms.Select(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.NumberInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        }




