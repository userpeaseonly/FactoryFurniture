from django import forms
from .models import Dealer, Product, DeliveryType

class DealerForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = ['name', 'phone_number1', 'phone_number2', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Dealer Name'}),
            'phone_number1': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number 1'}),
            'phone_number2': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number 2'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Address', 'rows': 3}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Product Name'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Price'}),
        }



class OrderStepOneForm(forms.Form):
    dealer = forms.ModelChoiceField(queryset=Dealer.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))

class OrderStepTwoForm(forms.Form):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox'})
    )

class OrderStepThreeForm(forms.Form):
    delivery_type = forms.ChoiceField(
        choices=DeliveryType.choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class OrderStepFourForm(forms.Form):
    delivery_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}))
    order_cost = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Order Cost'}))

class OrderStepFiveForm(forms.Form):
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Comment (Optional)', 'rows': 3})
    )