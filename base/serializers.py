from rest_framework import serializers


class GetInvoiceSimpleSerializer(serializers.Serializer):
    amount = serializers.CharField(required=True, allow_blank=False, max_length=15)

class GetInvoiceSerializer(serializers.Serializer):
    amount = serializers.CharField(required=True, allow_blank=False, max_length=15)
    description = serializers.CharField(required=True, allow_blank=False, max_length=45)
    callback_url = serializers.CharField(required=True, allow_blank=False, max_length=45)
    receiver_data = serializers.CharField(required=True, allow_blank=False, max_length=45)