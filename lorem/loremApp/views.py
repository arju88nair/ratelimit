from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
from ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='1/m', block=True)
@api_view(["GET"])
def localScope(request):
    try:
        return JsonResponse("Lorem ipsum blah",safe=False)
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

