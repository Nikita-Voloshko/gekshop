from django import forms

from orderapp.models import OrderItem


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()

    price = forms.CharField(label='цена', required=False)

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.item:
            field.widget.attrs['class'] = 'form-control'
