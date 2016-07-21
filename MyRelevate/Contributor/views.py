from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.forms import modelformset_factory

from .forms import ContributorForm, CredentialForm, AreaOfExpertiseForm, BiographyForm, InterestForm, ContactForm, \
    ApprovalContributorForm, ApprovalUpdateUserForm

from ..models import Topics, Pending
from models import ContributorProfile
from ..models import User


def index(request):
    if not request.user.is_contributor:
        return HttpResponseRedirect(reverse('myrelevate:index'))
    return render(request, 'articles.html', {'form': None})


@login_required()
def create(request):
    """
    Allows user to apply to get become a contributor
    :param request:
    :return: redirect to index page
    """
    if request.method == 'POST':
        form = ContributorForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save(email=request.user.email)
            user = get_user_model().objects.get(email=request.user.email)
            pending = Pending()
            contributor_profile = form.save()
            user.contributor_profile = contributor_profile
            pending.needApproval = user
            pending.save()
            # user.has_applied = True
            # user.is_contributor = True
            user.save()
            return HttpResponseRedirect(reverse('myrelevate:index'))
        else:
            return HttpResponse(form.errors)
    else:
        contributorForm = ContributorForm()
    return render(request, 'application.html', {'contributorForm': contributorForm})


@login_required()
def update(request):
    """
    Allows a user with contributor access to edit their contributor profile page
    Allows a contributor to post new articles
    :param request:
    :return: a redirect to contributor profile page
    """
    if request.method == 'POST':
        user = get_user_model().objects.get(email=request.user.email)
        form = ContributorForm(request.POST, request.FILES, instance=user.contributor_profile)
        if form.is_valid():
            # profile = ContributorProfile(cv=request.FILES['cv'])
            # form.save(email=request.user.email)
            form.save()
            return HttpResponseRedirect(reverse('myrelevate:contributor_profile'))
        else:
            return HttpResponse(form.errors)
    else:
        user = get_user_model().objects.get(email=request.user.email)
        profile = user.get_contributor_profile()
        topics = Topics.objects.all()
    return render(request, 'contributorprofile.html', {'contributorProfile': profile,
                                                       'topics': topics,
                                                       'contributorForm': ContributorForm(instance=profile),
                                                       'credenrialForm': CredentialForm(instance=profile),
                                                       # 'expertiseForm': AreaOfExpertiseForm(instance=profile),
                                                       'biographyForm': BiographyForm(instance=profile),
                                                       'interestForm': InterestForm(instance=profile),
                                                       'contactForm': ContactForm(instance=profile)})


@login_required()
def updateCredentials(request):
    if request.method == 'POST':
        form = CredentialForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def updateAreaOfExpertise(request):
    if request.method == 'POST':
        form = AreaOfExpertiseForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def updateBiography(request):
    if request.method == 'POST':
        form = BiographyForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def updateInterest(request):
    if request.method == 'POST':
        form = InterestForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def updateContact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=request.user.contributor_profile)
        if form.is_valid:
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:update'))


@login_required()
def remove(request):
    pass

@login_required()
def showpdf(request):
    user = get_user_model().objects.get(email=request.user.email)
    pro = user.get_contributor_profile()
    profile = ContributorProfile.objects.get(id=user.contributor_profile.pk)
    filepath = profile.cv.path
    filename = profile.cv.name
    fp = pro.cv.path
    # response = HttpResponse(open(filepath, 'rb'), content_type='application/pdf')
    # response['Content-Disposition'] = 'inline; filename="test_cv_resume_BYRIncf.pdf"'
    # p = canvas.Canvas(response)
    # # p.drawString(100, 100, "Hello world.")
    # p.getpdfdata()
    # p.showPage()
    # p.save()
    # with open(filename, 'wb') as pdf:
    #     response = HttpResponse(content_type='application/pdf')
    #     response['Content-Disposition'] = 'filename="test_cv_resume_BYRIncf.pdf"'
    #     p = canvas.Canvas(response)
    #     pdf.write(p.getpdfdata())
    # with open(filepath, 'rb') as pdf:
    #     response = HttpResponse(pdf.read(), content_type='application/pdf')
    #     response['Content-Disposition'] = 'inline; filename="test_cv_resume_BYRIncf.pdf"'
        # p = canvas.Canvas(response)
        # p.showPage()
        # p.save()
    pdf_data = open(filepath, 'rb').read()
    return HttpResponse(pdf_data, content_type="application/pdf")


def contributors(request):
    """
    Displays list of all contributors.
    Allows a person to search contributors based on a set of given topics
    :param request:
    :return: The requested searched data
    """
    users = get_user_model().objects.all()
    contributor_profiles = get_user_model().objects.all()
    if request.method == 'GET':
        if 'q' in request.GET and request.GET['q']:
            q = request.GET['q']
            profiles = users.filter(first_name__icontains=q)
            return render(request, 'contributors.html', {'profiles': profiles, 'query': q})
        else:
            pass
    else:
        pass
    return render(request, 'contributors.html', {'contributors': contributor_profiles})


@login_required()
def approve(request):
    pending_ids = Pending.objects.values_list('needApproval_id', flat=True)
    profile_ids = User.objects.values_list('contributor_profile_id', flat=True)
    users = User.objects.filter(id__in=pending_ids)
    profiles = ContributorProfile.objects.filter(id__in=profile_ids)
    ApproveFormSet = modelformset_factory(User, form=ApprovalUpdateUserForm, extra=0)
    data = {
        'form-TOTAL_FORMS': pending_ids.count(),
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '',
    }
    if request.method == 'POST':
        formset = ApproveFormSet(request.POST, queryset=users)
        # user_id = request.POST.get('user_id')
        # user = User.objects.get(id=user_id)
        # form = ApprovalUpdateUserForm(request.POST, instance=user)
        if formset.is_valid():
            formset.save()
            # form.save()
            return HttpResponseRedirect(reverse('myrelevate:contributor:approve'))
        else:
            print formset.errors
    else:
        formset = ApproveFormSet(queryset=users)
    return render(request, 'approval.html', {'profiles': profiles, 'users': users, 'formset': formset})


@login_required()
def update_user_contributor(request):
    if request.method == 'POST':
        form = ApprovalUpdateUserForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print form.errors
    return HttpResponseRedirect(reverse('myrelevate:contributor:approval'))


# @login_required()
# def approve(request,id):
#     user = get_user_model().objects.get(email=id)
#     if request.method == 'POST':
#         form = ApprovalContributorForm(request.POST, request.FILES, instance=user.contributor_profile)
#         form2 = ApprovalUpdateUserForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save(email=request.user.email)
#             return HttpResponseRedirect(reverse('myrelevate:contributor_profile'))
#         else:
#             return HttpResponse(form.errors)
#     else:
#         user = get_user_model().objects.get(email=id)
#         profile = user.get_contributor_profile()
#     return render(request, 'approvalcontributorprofile.html', {'contributorProfile': profile,
#                                                        'approvalContributorForm': ApprovalContributorForm(instance=profile),
#                                                        'approvalUpdateUserForm': ApprovalUpdateUserForm(instance=profile),
#                                                                })


