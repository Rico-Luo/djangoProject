1. 项目设置 (djangoProject/settings.py)
```
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your_secret_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 确保这里包含了所有模板文件所在的位置
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoProject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'guoyu-soar',
        'USER': 'root',
        'PASSWORD': 'Fangyu@123!',
        'HOST': '10.7.0.109',  # 或者你的数据库主机地址
        'PORT': '3306',  # 默认端口
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```
2. 应用配置 (user/apps.py)
```
from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
```
3. 模型 (user/models.py)
```
from django.db import models

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name
```
4. 表单 (user/forms.py)
```
from django import forms
from .models import User

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'email']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'email']
```
5. 视图 (user/views.py)
```
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

    return render(request, 'user/user_list.html', {'page_obj': page_obj, 'query': query})

def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserCreateForm()
    return render(request, 'user/user_create.html', {'form': form, 'title': 'Create User'})

def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'user/user_form.html', {'form': form, 'title': 'Edit User'})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user/user_confirm_delete.html', {'user': user})
```
6. URL 配置 (user/urls.py)
```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('create/', views.user_create, name='user_create'),
    path('edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('delete/<int:pk>/', views.user_delete, name='user_delete'),
]
```
7. 项目 URL 配置 (djangoProject/urls.py)
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
]
```
8. 模板文件
user/user_list.html
```
<!DOCTYPE html>
<html>
<head>
    <title>User List</title>
</head>
<body>
    <h1>User List</h1>
    <form method="get" style="margin-bottom: 10px;">
        <input type="text" name="q" value="{{ query }}" placeholder="Search by username or email">
        <button type="submit">Search</button>
    </form>
    <a href="{% url 'user_create' %}">Add User</a>
    <table border="1">
        <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Registration Date</th>
            <th>Actions</th>
        </tr>
        {% for user in page_obj %}
        <tr>
            <td>{{ user.user_name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.created_at }}</td>
            <td>
                <a href="{% url 'user_edit' user.id %}">Edit</a>
                <a href="{% url 'user_delete' user.id %}">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </table>
    <div class="pagination">
        <span class="step-links">
            {% if page_obj.has_previous %}
                <a href="?page=1{% if query %}&q={{ query }}{% endif %}">&laquo; first</a>
                <a href="?page={{ page_obj.previous_page_number }}{% if query %}&q={{ query }}{% endif %}">previous</a>
            {% endif %}
            
            <span class="current">
                Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
            </span>
            
            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}{% if query %}&q={{ query }}{% endif %}">next</a>
                <a href="?page={{ page_obj.paginator.num_pages }}{% if query %}&q={{ query }}{% endif %}">last &raquo;</a>
            {% endif %}
        </span>
    </div>
</body>
</html>
```
user/user_create.html
```
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Create</button>
    </form>
    <a href="{% url 'user_list' %}">Back to User List</a>
</body>
</html>
user/user_form.html
html
浅色版本
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Save</button>
    </form>
    <a href="{% url 'user_list' %}">Back to User List</a>
</body>
</html>
```
user/user_confirm_delete.html
```
<!DOCTYPE html>
<html>
<head>
    <title>Delete User</title>
</head>
<body>
    <h1>Delete User</h1>
    <p>Are you sure you want to delete the user "{{ user.user_name }}"?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit">Delete</button>
        <a href="{% url 'user_list' %}">Cancel</a>
    </form>
</body>
</html>
```
9. 运行迁移
确保数据库迁移已经运行：
```
python manage.py makemigrations
python manage.py migrate
```
10. 启动服务器
启动 Django 开发服务器：
```
python manage.py runserver
```
11. 访问用户管理界面
打开浏览器，访问 http://127.0.0.1:8000/user/ 即可看到用户管理界面。