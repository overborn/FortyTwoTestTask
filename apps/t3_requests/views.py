from django.shortcuts import render


def requests(request, template='requests.html'):
    return render(request, template)
