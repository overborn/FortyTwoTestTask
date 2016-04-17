from django.shortcuts import render


def edit(request, template='edit.html'):
    return render(request, template)
