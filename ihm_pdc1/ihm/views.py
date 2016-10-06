from django.shortcuts import render
from .backend.vocabulary import bleu

# Create your views here.

def search(request):
    a = bleu()
    return render(request, 'search.html', {'test':a})