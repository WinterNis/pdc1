from django.shortcuts import render
from .testing.testing import bleu

# Create your views here.

def search(request):
    a = bleu()
    return render(request, 'search.html', {'test':a})