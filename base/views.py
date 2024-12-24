import os
import json
import logging
import base64
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden


from base import serializers
from base import exceptions

from base.utils import create_invoice_simple
from base.utils import create_invoice


def ping(request):
    return JsonResponse({
        'module': 'QPAY TV',
        'version': os.environ.get('IMAGE_VERSION', ''),
        'build_mode': os.environ.get('BUILD_MODE', ''),
        'build_date': os.environ.get('BUILD_DATE', '')
    })


class GetinvoiceSimpleView(APIView):
    
    def post(self, request, format=None):
        serializer = serializers.GetInvoiceSimpleSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            print("data : ", data)
            response = create_invoice_simple(data)
            return Response(response)
        raise exceptions.RequestDataValidationException(
            detail_data=serializer.errors,
            log_data={"request_data": request.data, "errors": serializer.errors}
        )

class GetinvoiceView(APIView):
    
    def post(self, request, format=None):
        serializer = serializers.GetInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            print("data : ", data)
            response = create_invoice(data)
            return Response(response)
        raise exceptions.RequestDataValidationException(
            detail_data=serializer.errors,
            log_data={"request_data": request.data, "errors": serializer.errors}
        )


class CancelInvoiceView(APIView):
    
    def post(self, request, format=None):
        serializer = serializers.GetInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            print("data : ", data)
            response = create_invoice_test(data)
            return Response(response)
        raise exceptions.RequestDataValidationException(
            detail_data=serializer.errors,
            log_data={"request_data": request.data, "errors": serializer.errors}
        )

class GetPaymentView(APIView):
    
    def post(self, request, format=None):
        serializer = serializers.GetInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            print("data : ", data)
            response = create_invoice_test(data)
            return Response(response)
        raise exceptions.RequestDataValidationException(
            detail_data=serializer.errors,
            log_data={"request_data": request.data, "errors": serializer.errors}
        )

class CheckPaymentView(APIView):
    
    def post(self, request, format=None):
        serializer = serializers.GetInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            print("data : ", data)
            response = create_invoice_test(data)
            return Response(response)
        raise exceptions.RequestDataValidationException(
            detail_data=serializer.errors,
            log_data={"request_data": request.data, "errors": serializer.errors}
        )

class CancelPaymentView(APIView):
    
    def post(self, request, format=None):
        serializer = serializers.GetInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            print("data : ", data)
            response = create_invoice_test(data)
            return Response(response)
        raise exceptions.RequestDataValidationException(
            detail_data=serializer.errors,
            log_data={"request_data": request.data, "errors": serializer.errors}
        )

class RefundPaymentView(APIView):
    
    def post(self, request, format=None):
        serializer = serializers.GetInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            print("data : ", data)
            response = create_invoice_test(data)
            return Response(response)
        raise exceptions.RequestDataValidationException(
            detail_data=serializer.errors,
            log_data={"request_data": request.data, "errors": serializer.errors}
        )

class PaymentListView(APIView):
    
    def post(self, request, format=None):
        serializer = serializers.GetInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            print("data : ", data)
            response = create_invoice_test(data)
            return Response(response)
        raise exceptions.RequestDataValidationException(
            detail_data=serializer.errors,
            log_data={"request_data": request.data, "errors": serializer.errors}
        )