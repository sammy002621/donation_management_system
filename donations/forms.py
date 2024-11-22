from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    is_anonymous = forms.BooleanField(required=False, initial=False,
                                    label='Make donation anonymous')
    
    class Meta:
        model = Donation
        fields = ['donor', 'event', 'amount', 'payment_method', 'is_anonymous', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs and 'donor' in kwargs['initial']:
            self.fields['donor'].widget = forms.HiddenInput()
        if 'initial' in kwargs and 'event' in kwargs['initial']:
            self.fields['event'].widget = forms.HiddenInput()