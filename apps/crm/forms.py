from django import forms 

from apps.crm.models import Billing

class BillingForm(forms.ModelForm):
    created_display = forms.DateTimeField(
        label="Дата создания",
        required=False,
        widget=forms.DateTimeInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = Billing
        fields = (
            'billing_type', 'billing_receipt_type', 'billing_status', 'billing_payment_status',
            'billing_payment', 'user', 'email', 'first_name', 'last_name', 'phone',
            'payment_code', 'country', 'region', 'street', 'apartment', 'zip_code', 'note',
            'delivery_price', 'discount_price', 'client_gave_money', 'change_price',
            'total_price',
        )
        # widgets = {
        #     'delivery_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        # }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if request and request.user.is_authenticated:
            self.fields['user'].initial = request.user.id

        if self.instance and self.instance.id:
            self.fields['created_display'].initial = self.instance.created
            self.fields['created_display'].disabled = True
            
            readonly_fields = (
               'delivery_price', 'discount_price', 'client_gave_money',
                'change_price', 'payment_code', 'total_price', 'user',
            )
            for field_name in readonly_fields:
                self.fields[field_name].disabled = True
        else:
            self.fields.pop('created_display')