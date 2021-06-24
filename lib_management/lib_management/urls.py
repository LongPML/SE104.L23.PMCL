from django.contrib import admin
from django.urls import include, path

from library.views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('book/add', BookAdd),
    path('bookEdit/<int:id_b>', BookEdit),
    path('bookEdit/bookUpdate',BookUpdate),
    path('card/add', CardAdd),
    path('member/add', MemberAdd),
    path('memberDetail',MemberDetail),
    path('cardDetail/',CardDetail),
    path('cardEdit/<int:id_bc>',CardEdit),
    path('cardEdit/cardUpdate',CardUpdate),
    path('bookDetail/',BookDetail),
    path('login/',Login),
    path('admin/',admin_home),
]