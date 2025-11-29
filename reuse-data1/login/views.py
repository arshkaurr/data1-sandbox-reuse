from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def logout(request):
    logout(request)
    return redirect('HOME')
    # return HttpResponse('WORING - LOGOUT PAGE')
