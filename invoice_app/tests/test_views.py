from invoice_server.invoice_app.models import InvoiceDetail
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
    
  
    
    def test_update_invoice_with_invoice_details(self):
        # Create an initial invoice with some details
        initial_invoice = InvoiceFactory.create()
        initial_details = [
            {
                "description": "Initial Product",
                "quantity": 1,
                "unit_price": 20.0,
            }
        ]
        for detail_data in initial_details:
            InvoiceDetail.objects.create(invoice=initial_invoice, **detail_data)

        # Define the updated invoice data
        updated_invoice_data = {
            "date": "2023-09-26",
            "customer_name": "Updated Customer",
            "invoice_details": [
                {
                    "id": initial_invoice.invoice_details.first().id,  
                    "description": "Updated Product",
                    "quantity": 3,
                    "unit_price": 15.0,
                },
                {
                    
                    "description": "New Product",
                    "quantity": 2,
                    "unit_price": 10.0,
                },
            ],
        }

        # Prepare the URL for updating the invoice
        url = reverse('invoice-detail', kwargs={'pk': initial_invoice.pk})

        # Send a PUT request to update the invoice
        response = self.client.put(url, data=updated_invoice_data, format="json")

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the initial invoice instance from the database
        initial_invoice.refresh_from_db()

        # Check if the invoice and details are updated correctly
        self.assertEqual(initial_invoice.date, "2023-09-26")
        self.assertEqual(initial_invoice.customer_name, "Updated Customer")

        # Check the updated detail
        updated_detail = initial_invoice.invoice_details.first()
        self.assertEqual(updated_detail.description, "Updated Product")
        self.assertEqual(updated_detail.quantity, 3)
        self.assertEqual(updated_detail.unit_price, 15.0)

        # Check the newly created detail
        new_detail = initial_invoice.invoice_details.last()
        self.assertEqual(new_detail.description, "New Product")
        self.assertEqual(new_detail.quantity, 2)
        self.assertEqual(new_detail.unit_price, 10.0)
