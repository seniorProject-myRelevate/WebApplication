from django.shortcuts import render
from django.http import HttpResponse

from .forms import RegistrationForm


def index(request):
    form = RegistrationForm()
    return render(request, 'index.html', {'form': form})
