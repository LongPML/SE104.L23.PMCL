from django.contrib import admin
from django.urls import include, path

from library.views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('searchbook/', search_book,),
    path('admin/', admin.site.urls),
    path('adminlogin/', admin_login),
    path('book/add', BookAdd)
]