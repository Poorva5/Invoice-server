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
        fields = ['id', 'date', 'customer_name', 'created_at', 'updated_at', 'invoice_details']
        
        
    def create(self, validated_data):
        invoice_details = validated_data.pop('invoice_details')
        invoice = Invoice.objects.create(**validated_data)
        for detail in invoice_details:
            InvoiceDetail.objects.create(invoice=invoice, **detail)
        return invoice
    