from utils.test_utils import APITest
from rest_framework import status
from django.urls import reverse
from invoice_app.factory import InvoiceFactory
from invoice_app.models import Invoice

class InvoiceTestCase(APITest):
    def setUp(self):
        self.url = '/api/invoice/'
        self.invoice_data = {
            "date": "2023-09-25",
            "customer_name": "John",
            "invoice_details": [
                {
                    "description": "Product 1",
                    "quantity": 5,
                    "unit_price": 10.0,
                },
                {
                    "description": "Product 2",
                    "quantity": 3,
                    "unit_price": 15.0,
                },
            ],
        }
    def test_create_invoice(self):
        response = self.client.post(self.url, data=self.invoice_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)

        invoice = Invoice.objects.first()
        self.assertEqual(invoice.customer_name, "John")
        self.assertEqual(invoice.invoice_details.count(), 2)
        
    def test_list_invoices(self):
        InvoiceFactory.create_batch(3)
        response = self.client.get(self.url)
        
        self.assertEqual(len(response.data), 3) 
    
  