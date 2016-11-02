from django.shortcuts import render
from .backend.run import generate_index, search_words
import re

# Create your views here.


def generate(request):
    if request.method == 'POST':
        generate_index()
        generated = True

    return render(request, 'index.html', locals())


def search(request):
    if request.method == 'POST':
        # the called function is making a read to the disk each time, it could be interesting to cache it
        results = search_words(request.POST.get('search'))

        for result in results:
            for word in request.POST.get('search').split(' '):
                result[2] = result[2].replace(word, "<span class=\'highlight_word\'>"+word+"</span>")

    return render(request, 'search.html', locals())
