from django.shortcuts import render

# Create your views here.
def privacy_policy(request):
    # return render(request, 'privacy.html')
    return render(request, 'new.html')


def accountdeleteView(request):
    return render(request, 'accountDelete.html')