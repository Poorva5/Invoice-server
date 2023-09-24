import re
from rest_framework import serializers
from invoice_app.models import Invoice, InvoiceDetail


class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = ['id', 'description', 'quantity', 'unit_price', 'price', 'created_at', 'updated_at']
        

class InvoiceSerializer(serializers.ModelSerializer):
    invoice_details = InvoiceDetailSerializer(many=True)
    
    class Meta:
        model = Invoice
        fields = ['id', 'date', 'customer_name', 'created_at', 'updated_at','invoice_details']
        
        
    def create(self, validated_data):
        invoice_details = validated_data.pop('invoice_details', [])
        invoice = Invoice.objects.create(**validated_data)
        for detail in invoice_details:
            InvoiceDetail.objects.create(invoice=invoice, **detail)
        return invoice
    
    
    def update(self, instance, validated_data):
        invoice_details_data = validated_data.pop('invoice_details', [])

        # Update invoice fields
        instance.date = validated_data.get('date', instance.date)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.save()

        # Update or create invoice details
        for detail_data in invoice_details_data:
            detail_id = detail_data.get('id')
            if detail_id:
                # If an ID is provided, update the existing invoice detail
                detail = InvoiceDetail.objects.get(id=detail_id, invoice=instance)
                detail.description = detail_data.get('description', detail.description)
                detail.quantity = detail_data.get('quantity', detail.quantity)
                detail.unit_price = detail_data.get('unit_price', detail.unit_price)
                detail.save()
            else:
                # If no ID is provided, create a new invoice detail
                InvoiceDetail.objects.create(invoice=instance, **detail_data)

        return instance
    