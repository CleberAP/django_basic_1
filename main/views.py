from django.shortcuts import render

def index(request):
    template = 'main/home.html'

    context = {}

    return render(request, template, context)


