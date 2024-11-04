from django import forms
from .models import Cargo
from .constants import CARGO_TRACKING_URLS

class CargoForm(forms.ModelForm):
    carrier_name = forms.ChoiceField(
        choices=[(key, key) for key in CARGO_TRACKING_URLS.keys()],
        label="Kargo Firması"
    )

    class Meta:
        model = Cargo
        fields = ['carrier_name', 'tracking_number']
