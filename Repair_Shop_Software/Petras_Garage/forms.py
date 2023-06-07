from django import forms
from . import models


class OrderMessageForm(forms.ModelForm):
    class Meta:
        model = models.OrderMessage
        fields = ('content', 'order', 'messenger')
        widgets = {
            'order': forms.HiddenInput(),
            'messenger': forms.HiddenInput(),

        }