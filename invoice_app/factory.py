import factory
from .models import Invoice, InvoiceDetail


class InvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Invoice
        
    date = factory.Faker('date_time_this_decade') 
    customer_name = factory.Faker('name')

    def __str__(self):
        return self.customer_name
    
class InvoiceDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InvoiceDetail

    invoice = factory.SubFactory(InvoiceFactory)
    description = factory.Faker('text')
    quantity = factory.Faker('random_int', min=1, max=10)
    unit_price = factory.Faker('random_number', digits=10)
    price = factory.LazyAttribute(lambda obj: obj.quantity * obj.unit_price)
