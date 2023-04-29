from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
def gardening_calculator(request):
    return render(request,'gardening_calculator.html')