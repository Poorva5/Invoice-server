from django.db import models
from utils.models import BaseModel


class Invoice(BaseModel):
    date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.customer_name
    

class InvoiceDetail(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,  related_name='invoice_details')
    description = models.TextField()
    quantity = models.IntegerField()
    unit_price = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    
    def __str__(self):
        return f'{self.invoice.pk} - {self.description}'