from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'payment']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(OrderForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(OrderForm, self).save(commit=False)
        if self.user:
            instance.client = self.user
        if commit:
            instance.save()
        return instance
