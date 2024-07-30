from django.contrib import admin
from django.urls import path, include

from .views import Login, Register, UserMainPage, Logout, EditUserProfile, reset_password, reset_password_confirm, reset_password_complete

urlpatterns = [
    path('login', Login),
    path('register', Register),
    path('user', UserMainPage),
    path('logout', Logout),
    path('user/edit', EditUserProfile),
    path('reset-password/', reset_password),
    path('reset-password/<tokenid>', reset_password_confirm),
    path('reset-password/<tokenid>/<code>', reset_password_complete)
]
