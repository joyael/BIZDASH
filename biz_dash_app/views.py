from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,  get_object_or_404
from .models import CustomUser 
from .operations_by_role import operations
from django.contrib import messages
from .forms import CustomUserForm


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page

@login_required
def admin_report(request):
    # Ensure the user is authenticated and has the correct role
    if request.user.role == 'admin':
        users = CustomUser .objects.all()
        managers = CustomUser .objects.filter(role='manager')
        staffs = CustomUser .objects.filter(role='staff')
        userscount = users.count()
        managerscount = managers.count()
        staffscount = staffs.count()
        operations1 = operations['admin']

        return render(request, 'admin_report.html', {  # Corrected render call
            'userscount': userscount,
            'managerscount': managerscount,
            'staffscount': staffscount,
            'operations': operations1,
        })

    else:
        return redirect('login')  # Redirect to login page if not an admin
    
@login_required
def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.manager = request.user  # Set the current user as the manager
            user.save()
            messages.success(request, 'User  added successfully.')
            return redirect('view_users')  # Redirect to a user list or another page
    else:
        form = CustomUserForm()
    return render(request, 'add_user.html', {'form': form})


@login_required
def view_user(request, user_id):
    user = get_object_or_404(CustomUser , id=user_id)
    return render(request, 'view_user.html', {'user': user})

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser , id=user_id)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User  updated successfully.')
            return redirect('view_users')  # Redirect to a user list or another page
    else:
        form = CustomUserForm(instance=user)
    return render(request, 'edit_user.html', {'form': form, 'user': user})


@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser , id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User  deleted successfully.')
        return redirect('view_users')  # Redirect to a user list or another page
    return render(request, 'delete_user.html', {'user': user})
