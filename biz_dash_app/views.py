from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,  get_object_or_404
from .models import CustomUser , Report
from .operations_by_role import operations
from django.contrib import messages
from .forms import CustomUserForm, ReportForm
from django.core.exceptions import PermissionDenied


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'manager':
                return redirect('manager_home')
            elif user.role == 'staff':
                return redirect('staff_home')  # Redirect to a success page
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
        users = CustomUser.objects.all()
        managers = CustomUser.objects.filter(role='manager')
        staffs = CustomUser.objects.filter(role='staff')
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
    if not request.user.role == 'manager':
        messages.error('Not a manager')
        return redirect('login')
    operations1 = operations['manager']
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.manager = request.user  # Set the current user as the manager
            raw_password = form.cleaned_data['password']
            user.set_password(raw_password)
            user.save()
            messages.success(request, 'User  added successfully.')
            return redirect('view_staffs')  # Redirect to a user list or another page
    else:
        form = CustomUserForm()
    return render(request, 'staff_manage/add_user.html', {'form': form, 'operations': operations1,})


@login_required
def view_user(request, user_id):
    if not (request.user.role == 'manager' or 'admin'):
        messages.error('Not a manager')
        return redirect('login')
    
    operations1 = operations[request.user.role]
    user = get_object_or_404(CustomUser , id=user_id)
    return render(request, 'staff_manage/view_user.html', {'user': user, 'operations': operations1,})

@login_required
def edit_user(request, user_id):
    if not request.user.role == 'manager':
        messages.error('Not a manager')
        return redirect('login')
    operations1 = operations[request.user.role]
    user = get_object_or_404(CustomUser , id=user_id)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User  updated successfully.')
            return redirect('view_staffs')  # Redirect to a user list or another page
    else:
        form = CustomUserForm(instance=user)
    return render(request, 'staff_manage/edit_user.html', {'form': form, 'user': user, 'operations': operations1,})


@login_required
def delete_user(request, user_id):
    if not request.user.role == 'manager':
        messages.error('Not a manager')
        return redirect('login')
    operations1 = operations[request.user.role]
    user = get_object_or_404(CustomUser , id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User  deleted successfully.')
        return redirect('view_staffs')  # Redirect to a user list or another page
    return render(request, 'staff_manage/delete_user.html', {'user': user, 'operations': operations1,})

@login_required
def view_staffs(request):
    if not request.user.role == 'manager':
        messages.error('Not a manager')
        return redirect('login')
    manager = request.user
    operations1 = operations[request.user.role]
    users = CustomUser .objects.filter(role='staff',manager=manager)
    return render(request, 'staff_manage/view_staffs.html', {'users': users, 'operations': operations1,})


@login_required
def add_report(request):
    if not request.user.role == 'staff':
        messages.error('Not a Staff')
        return redirect('login')
    operations1 = operations[request.user.role]
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            report = form.save(commit=False)
            report.staff = request.user  # Set the current user as the manager
            report.save()
            messages.success(request, 'Report added successfully.')
            return redirect('view_reports')  # Redirect to the report list or another page
    else:
        form = ReportForm()
    return render(request, 'report/add_report.html', {'form': form, 'operations': operations1,})


@login_required
def view_report(request, report_id):
    operations1 = operations[request.user.role]
    report = get_object_or_404(Report, id=report_id)
    return render(request, 'report/view_report.html', {'report': report, 'operations': operations1,})


@login_required
def edit_report(request, report_id):
    if not request.user.role == 'staff':
        messages.error('Not a Staff')
        return redirect('login')
    operations1 = operations[request.user.role]
    report = get_object_or_404(Report, id=report_id)
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            messages.success(request, 'Report updated successfully.')
            return redirect('view_reports')  # Redirect to the report list or another page
    else:
        form = ReportForm(instance=report)
    return render(request, 'report/edit_report.html', {'form': form, 'report': report, 'operations': operations1,})


@login_required
def delete_report(request, report_id):
    if not request.user.role == 'staff':
        messages.error('Not a Staff')
        return redirect('login')
    operations1 = operations[request.user.role]
    report = get_object_or_404(Report, id=report_id)
    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Report deleted successfully.')
        return redirect('view_reports')  # Redirect to the report list or another page
    return render(request, 'report/delete_report.html', {'report': report, 'operations': operations1,})


@login_required
def reports_staff_view(request):
    if not request.user.role == 'staff':
        messages.error('Not a Staff')
        return redirect('login')
    operations1 = operations[request.user.role]
    # Retrieve all reports from the database
    reports = Report.objects.filter(staff=request.user)
    # Render the template with the reports context
    return render(request, 'reports_staff_view.html', {'reports': reports, 'operations': operations1,})

@login_required
def reports_manager_view(request):
    if not request.user.role == 'manager':
        messages.error('Not a manager')
        return redirect('login')
    operations1 = operations[request.user.role]
    # Get the current user (manager)
    manager = request.user
    # Get all staff members under this manager
    staff_members = CustomUser .objects.filter(manager=manager)
    # Get reports for the staff members under this manager
    reports = Report.objects.filter(staff__in=staff_members)
    # Render the template with the list of reports
    return render(request, 'reports_manager_view.html', {'reports': reports, 'operations': operations1,})


@login_required
def manager_home_view(request):
    if not request.user.role == 'manager':
        messages.error('Not a manager')
        return redirect('login')
    operations1 = operations[request.user.role]
    manager = request.user
    staff_members = CustomUser.objects.filter(manager=manager)
    staff_count = staff_members.count()
    reports = Report.objects.filter(staff__in=staff_members)
    approved_count = reports.filter(status='approved').count()
    rejected_count = reports.filter(status='rejected').count()
    pending_count = reports.filter(status='pending').count()
    # Render the manager home page
    context = {
        'staff_count': staff_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'pending_count': pending_count, 
        'operations': operations1,
    }

    return render(request, 'manager_home.html', context)

@login_required
def approve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if request.user.role != 'manager' or report.staff.manager != request.user:
        raise PermissionDenied("You are not authorized to approve this report.")
    operations1 = operations[request.user.role]
    report.status = 'approved'
    report.save()
    messages.success(request, 'Report approved successfully.')
    return redirect('reports_manager_view', {'operations': operations1,})


@login_required
def reject_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if request.user.role != 'manager' or report.staff.manager != request.user:
        raise PermissionDenied("You are not authorized to reject this report.")
    operations1 = operations[request.user.role]
    report.status = 'rejected'
    report.save()
    messages.success(request, 'Report rejected successfully.')
    return redirect('reports_manager_view',{'operations': operations1,})