from django.contrib import admin
from django.urls import include, path

from library.views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('searchbook/', search_book,),
    path('admin/', admin.site.urls),
    path('adminlogin/', admin_login),
    path('book/add', BookAdd),
    path('book/update', BookUpdate),
    path('card/add', CardAdd),
    path('member/add', MemberAdd),
    path('memberDetail',MemberDetail),
    path('cardDetail',CardDetail),
    path('cardEdit/<int:id_bc>',CardEdit),
    path('cardEdit/cardUpdate',CardUpdate),
    path('bookDetail',BookDetail),
    path('login/',Login),
]