from django.contrib.auth import get_user_model
from django.shortcuts import render


def profile(request):
    """
    really just a test page. it isnt really anything yet.
    :param request:
    :return:
    """
    profile = get_user_model().objects.all()
    return render(request, 'userprofile.html', {'profile': profile})
