from django.shortcuts import render
<<<<<<< HEAD

# Create your views here.
=======
from django.http import HttpResponse

from .forms import RegistrationForm


def index(request):
    form = RegistrationForm()
    return render(request, 'index.html', {'form': form})
>>>>>>> c4bfe8e832acc437f2c1485cb6d163cc1675c7e3
