from django import forms

from .models import Computer, Lab


class LabForm(forms.ModelForm):
    class Meta:
        model = Lab
        fields = ["name", "room_number", "description"]


class ComputerForm(forms.ModelForm):
    class Meta:
        model = Computer
        fields = ["lab", "computer_number", "specifications", "status"]
