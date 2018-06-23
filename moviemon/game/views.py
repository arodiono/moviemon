from django.shortcuts import render


def index(request):
    title = 'TitleScreen'
    return render(request, 'index.html', locals())
