from django.shortcuts import render

def index(request):
    context = {}
    template = 'index_test.html'
    return render(request, template, context)
