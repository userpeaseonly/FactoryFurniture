from django import forms
from .models import Dealer, Product, DeliveryType

class DealerForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = ['name', 'phone_number1', 'phone_number2', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 placeholder-gray-400',
                'placeholder': 'Dealer Name'
            }),
            'phone_number1': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 placeholder-gray-400',
                'placeholder': 'Phone Number 1'
            }),
            'phone_number2': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 placeholder-gray-400',
                'placeholder': 'Phone Number 2'
            }),
            'address': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 placeholder-gray-400',
                'placeholder': 'Address',
                'rows': 3
            }),
        }



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 placeholder-gray-400',
                'placeholder': 'Product Name'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 placeholder-gray-400 mb-4',
                'placeholder': 'Price'
            }),
        }



class OrderStepOneForm(forms.Form):
    dealer = forms.ModelChoiceField(
        queryset=Dealer.objects.all(),
        widget=forms.Select(attrs={
            'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:w-auto',
        })
    )

class OrderStepTwoForm(forms.Form):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-checkbox h-5 w-5 text-blue-600 rounded focus:ring-blue-500 sm:h-6 sm:w-6',
        })
    )

class OrderStepThreeForm(forms.Form):
    delivery_type = forms.ChoiceField(
        choices=DeliveryType.choices,
        widget=forms.Select(attrs={
            'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:w-auto',
        })
    )

class OrderStepFourForm(forms.Form):
    delivery_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:w-auto',
            'type': 'date',
        })
    )
    order_cost = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:w-auto',
            'placeholder': 'Order Cost',
        })
    )

class OrderStepFiveForm(forms.Form):
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 placeholder-gray-400 sm:w-auto',
            'placeholder': 'Comment (Optional)',
            'rows': 3,
        })
    )
