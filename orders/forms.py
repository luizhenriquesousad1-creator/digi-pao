from django import forms
from .models import Order


class CheckoutForm(forms.Form):

    fulfillment_method = forms.ChoiceField(
        label='Modalidade de recebimento',
        choices=Order.FulfillmentMethod.choices,
        widget=forms.RadioSelect
    )

    payment_method = forms.ChoiceField(
        label='Forma de pagamento',
        choices=Order.PaymentMethod.choices,
        widget=forms.RadioSelect
    )

    delivery_address = forms.CharField(
        label='Endereço de entrega',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )

    def clean(self):

        cleaned_data = super().clean()

        fulfillment = cleaned_data.get('fulfillment_method')

        address = cleaned_data.get('delivery_address')

        if fulfillment == Order.FulfillmentMethod.DELIVERY and not address.strip():
            self.add_error(
                'delivery_address',
                'Informe o endereço para realizar a entrega.'
            )

        if fulfillment == Order.FulfillmentMethod.PICKUP:
            cleaned_data['delivery_address'] = ''

        return cleaned_data