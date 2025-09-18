from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Contact

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('contact_list')
        else:
            return render(request, 'contacts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'contacts/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def contact_list(request):
    contacts = Contact.objects.filter(user=request.user)
    return render(request, 'contacts/contact_list.html', {'contacts': contacts})

@login_required
def contact_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']
        Contact.objects.create(user=request.user, name=name, phone=phone, email=email, address=address)
        return redirect('contact_list')
    return render(request, 'contacts/contact_form.html')

@login_required
def contact_update(request, pk):
    contact = Contact.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        contact.name = request.POST['name']
        contact.phone = request.POST['phone']
        contact.email = request.POST['email']
        contact.address = request.POST['address']
        contact.save()
        return redirect('contact_list')
    return render(request, 'contacts/contact_form.html', {'contact': contact})

@login_required
def contact_delete(request, pk):
    contact = Contact.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'contacts/contact_delete.html', {'contact': contact})
