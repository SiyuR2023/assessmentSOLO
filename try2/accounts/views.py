from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.forms import ModelForm
from django_tables2 import RequestConfig
from django.urls import reverse  # 导入reverse用于动态解析URL
from .forms import CustomUserCreationForm, MassageLoginForm
from .models import Profile, Album, Review, Aoty
from .tables import AlbumTable

import csv
from django.core.paginator import Paginator


def homepage(request):
    return render(request, 'accounts/homepage.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('userpage'))  # 使用reverse动态获取URL
            else:
                form.add_error(None, "Invalid username or password")  # 明确添加错误信息
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/user_login.html', {'form': form})

def register(request):
    if request.session.get('is_login', None):  # 如果用户已登录，不允许注册
        return redirect('homepage')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # 保存User对象
           
            return HttpResponseRedirect(reverse('user_login'))  # 成功后跳转到用户页面
        else:
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})

def manager_login(request):
    if request.method == 'POST':
        form = MassageLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and (user.is_staff or user.is_superuser):
                login(request, user)
                return redirect('user_list')  # 重定向到管理员页面或其他适当的页面
            else:
                # 如果用户不存在或不是管理员，显示适当的错误消息
                form.add_error(None, 'Invalid credentials or not authorized as an administrator')
    else:
        form = MassageLoginForm()
    return render(request, 'accounts/manager_login.html', {'form': form})

def user_list(request):
    users = User.objects.all() 
    return render(request, 'admin/user_list.html')


def userpage(request):
    query = request.GET.get('query', '')
    if query:
        albums_list = Album.objects.filter(title__icontains=query)
    else:
        albums_list = Album.objects.all()

    paginator = Paginator(albums_list, 100)
    page_number = request.GET.get('page')
    albums = paginator.get_page(page_number)
    
    return render(request, 'element/userpage.html', {'albums': albums})

def add_to_cart(request, album_id):
    # 这里你可以添加逻辑来实现如何将专辑添加到购物车，例如使用 session
    cart = request.session.get('cart', [])
    if album_id not in cart:
        cart.append(album_id)
        request.session['cart'] = cart
        messages.success(request, "添加成功")
    else:
        messages.info(request, "此专辑已在购物车中")
    return redirect('album-list')  # 或者是你展示专辑的页面

def cart(request):
    cart = request.session.get('cart', [])
    # 根据 cart 中的 album_id 获取专辑详细信息，这需要从数据库查询
    albums = Album.objects.filter(id__in=cart)  # 假设你有一个 Album 模型
    return render(request, 'element/cart.html', {'albums': albums})

def album_detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    reviews = album.reviews.all()
    aoty_reviews = album.aoty_reviews.all()

    print(f"Album: {album}")
    print(f"Reviews: {reviews}")
    print(f"AOTY Reviews: {aoty_reviews}")
    return render(request, 'element/album_detail.html', {
        'album': album,
        'reviews': reviews,
        'aoty_reviews': aoty_reviews
    })

def review_list(request):
    reviews = Review.objects.select_related('album').all()
    return render(request, 'tests/reviews.html', {'reviews': reviews})

def aoty_list(request):
    aoty_reviews = Aoty.objects.select_related('album').all()
    return render(request, 'tests/aoty_reviews.html', {'aoty_reviews': aoty_reviews})


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['artist', 'title', 'release_date', 'format', 'label', 'genre']

# 显示专辑列表
def album_list(request):
    data = Album.objects.all()[:5000]  # 限制最多5000条数据
    table = AlbumTable(data)
    RequestConfig(request, paginate={"per_page": 50}).configure(table)  # 每页50条数据
    return render(request, 'admin/album_list.html', {'table': table})

# 添加新专辑
def album_add(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('album-list')
    else:
        form = AlbumForm()
    return render(request, 'admin/album_form.html', {'form': form})

# 编辑专辑
def album_edit(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            return redirect('album-list')
    else:
        form = AlbumForm(instance=album)
    return render(request, 'admin/album_form.html', {'form': form})

# 删除专辑
def album_delete(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        album.delete()
        return redirect('album-list')
    return render(request, 'admin/album_confirm_delete.html', {'object': album})

