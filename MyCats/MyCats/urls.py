from django.contrib import admin
from django.urls import include, path
from frontend_views import (
    home, login_view, logout_view, register_view,
    my_cats, add_cat, edit_cat, delete_cat,
    profile, edit_profile, change_password
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    # Frontend views
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('cats/', my_cats, name='my-cats'),
    path('cats/add/', add_cat, name='add-cat'),
    path('cats/<int:pk>/edit/', edit_cat, name='edit-cat'),
    path('cats/<int:pk>/delete/', delete_cat, name='delete-cat'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit-profile'),
    path('profile/change-password/', change_password, name='change-password'),
    path('chat/', chat, name='chat'),
]
