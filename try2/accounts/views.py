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
from django.db.models import Q
from .forms import CustomUserCreationForm, MassageLoginForm, PaymentForm
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
                return redirect('user_list')  
            else:
                
                form.add_error(None, 'Invalid credentials or not authorized as an administrator')
    else:
        form = MassageLoginForm()
    return render(request, 'accounts/manager_login.html', {'form': form})

def user_list(request):
    users = User.objects.all() 
    context = {'users': users}
    return render(request, 'admin/user_list.html', context)


def userpage(request):
    albums = None
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        print("Cart content:", cart)
        # Get the album details from the album_id in the cart, which requires a query from the database.
        albums = Album.objects.filter(id__in=cart)  
    query = request.GET.get('query', '')

    if query:
    # Construct a Q object with all possible search fields
        query_filters = Q(artist__icontains=query) | \
                        Q(title__icontains=query) | \
                        Q(release_date__icontains=query) | \
                        Q(format__icontains=query) | \
                        Q(label__icontains=query) | \
                        Q(genre__icontains=query)

    # Filter album listings based on constructed queries
        albums_list = Album.objects.filter(query_filters)
    else:
    # If there is no query string, all albums are returned
        albums_list = Album.objects.all()

    paginator = Paginator(albums_list, 100)
    page_number = request.GET.get('page')
    albums = paginator.get_page(page_number)
    
    return render(request, 'element/userpage.html', {'albums': albums})

def add_to_cart(request, album_id):
    cart = request.session.get('cart', [])
    if album_id not in cart:
        cart.append(album_id)
        request.session['cart'] = cart
        messages.success(request, "Successfully!")
    else:
        messages.info(request, "This album is in the shopping cart")
    return redirect('cart')  

def remove_from_cart(request, album_id):
    cart = request.session.get('cart', [])
    
    # Check if the album ID is in the shopping cart
    if album_id in cart:
        # Remove Album ID from Shopping Cart
        cart.remove(album_id)
        # Update shopping cart in session
        request.session['cart'] = cart
        # Add Success Message
        messages.success(request, "Album successfully removed from cart.")
    else:
        # Add an informative message if the album ID is not in the shopping cart
        messages.info(request, "Album not found in cart.")
    # Redirect to shopping cart page
    return redirect('cart')  # Here 'cart' should be the URL name of the page that displays the shopping cart

def cart(request):
    if request.method == 'POST':
        album_id = request.POST.get('album_id')  # Get album_id from POST request
        cart = request.session.get('cart', [])
        if album_id and album_id in cart:
            cart.remove(album_id)  # Remove Album ID from Shopping Cart
            request.session['cart'] = cart  # Update shopping cart in session
            messages.success(request, "Album successfully removed from cart.")
        else:
            messages.error(request, "Album not found in cart.")
        return redirect('cart')  # Redirection to avoid double submission of POST requests

    # GET Request Logic
    cart = request.session.get('cart', [])
    print("Cart content:", cart)
    albums = Album.objects.filter(id__in=cart) if cart else []
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

def album_list(request):
    data = Album.objects.all()[:5000]  # Limit to a maximum of 5000 pieces of data
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

# Edit Album
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

# Delete Album
def album_delete(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        album.delete()
        return redirect('album-list')
    return render(request, 'admin/album_confirm_delete.html', {'object': album})

def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # The actual payment logic can be integrated here
            request.session['cart'] = []  # The actual payment logic can be integrated here
            messages.success(request, "Payment successful and cart cleared.")
            return redirect('success')  # or redirect to another appropriate page
    else:
        form = PaymentForm()

    return render(request, 'element/payment.html', {'form': form})

def success(request):
    return render(request, 'element/success.html')


