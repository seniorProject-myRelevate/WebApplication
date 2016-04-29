from django.shortcuts import render

from forms import UserDataForm


def profile(request):
    """
    really just a test page. it isnt really anything yet.
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print form.errors
    return render(request, 'userprofile.html', {'userdata': UserDataForm(instance=request.user)})
