from orderapp.models import OrderItem


class OrderItemForm:
    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.item:
            field.widget.attrs['class'] = 'form-control'
