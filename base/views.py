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


def ping(request):
    return JsonResponse({
        'module': 'QPAY TV',
        'version': os.environ.get('IMAGE_VERSION', ''),
        'build_mode': os.environ.get('BUILD_MODE', ''),
        'build_date': os.environ.get('BUILD_DATE', '')
    })

def get_token():
    url = "https://merchant-sandbox.qpay.mn/v2/auth/token"

    payload = ""
    headers = {
        'Authorization': 'Basic'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print("response.text : ", response.text)
    ret = response.json()
    return ret


class GetInvioceView(APIView):
    
    def get(self, request, format=None):
        user_id = request.GET.get("user_id")
        print("request : ", request)
        
        token = get_token()
        print("token : ", token)
        
        return redirect(token)