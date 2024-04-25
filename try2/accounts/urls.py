from django.urls import path
from .views import homepage,user_login,register,manager_login,user_list,userpage,album_detail, review_list, aoty_list, album_list, album_add, album_edit, album_delete, add_to_cart, cart


urlpatterns = [
    path('', homepage, name='homepage'),
    path('user_login/', user_login, name='user_login'),
    path('register/', register, name='register'),
    path('manager_login/', manager_login, name='manager_login'),
    path('user_list.html/', user_list, name='user_list'),
    path('add-to-cart/<int:album_id>/', add_to_cart, name='add-to-cart'),
    path('userpage.html/', userpage, name='userpage'),
    path('album/<int:album_id>/', album_detail, name='album_detail'),
    path('reviews/', review_list, name='review-list'),
    path('aoty-reviews/', aoty_list, name='aoty-list'),
    path('albums/', album_list, name='album-list'),
    path('albums/add/', album_add, name='album-add'),
    path('albums/<int:pk>/edit/', album_edit, name='album-edit'),
    path('albums/<int:pk>/delete/', album_delete, name='album-delete'),
    path('cart/', cart, name='cart'),
]