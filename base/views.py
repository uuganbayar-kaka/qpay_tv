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
from base.utils import qpay_get_token
from base.utils import create_invoice_test


def ping(request):
    return JsonResponse({
        'module': 'QPAY TV',
        'version': os.environ.get('IMAGE_VERSION', ''),
        'build_mode': os.environ.get('BUILD_MODE', ''),
        'build_date': os.environ.get('BUILD_DATE', '')
    })


class GetInvioceView(APIView):
    
    def get(self, request, format=None):
        user_id = request.GET.get("user_id")
        print("request : ", request)
        
        token = qpay_get_token()
        response = create_invoice_test(token)
        print("response : ", response)
        
        return JsonResponse(response)