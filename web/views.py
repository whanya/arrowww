from django.shortcuts import render, redirect
from .forms import ContactRequestForm

def index(request):
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # потом сюда сделаем страницу-спасибо
    else:
        form = ContactRequestForm()

    return render(request, 'web/index.html', {'form': form})

def success(request):
    return render(request, 'web/success.html')

def privacy(request):
    return render(request, 'web/privacy.html')

def case0(request):
    return render(request, 'web/case0.html')

def case1(request):
    return render(request, 'web/case1.html')

def case2(request):
    return render(request, 'web/case2.html')