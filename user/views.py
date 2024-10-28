from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from .forms import UserCreateForm, UserEditForm
from django.core.paginator import Paginator
from django.db.models import Q

def user_list(request):
    query = request.GET.get('q')
    users = User.objects.all()

    if query:
        users = users.filter(
            Q(user_name__icontains=query) | Q(email__iexact=query)
        )

    paginator = Paginator(users, 10)  # 每页显示10个用户
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user_list.html', {'page_obj': page_obj, 'query': query})

def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserCreateForm()
    return render(request, 'user_create.html', {'form': form, 'title': 'Create User'})

def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'user_form.html', {'form': form, 'title': 'Edit User'})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})