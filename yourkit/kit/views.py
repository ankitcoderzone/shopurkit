from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
def home(request):
    return render(request, 'kit/index.html', {})