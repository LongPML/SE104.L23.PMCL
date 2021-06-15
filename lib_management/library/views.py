##### library.views.py
from django.shortcuts import render

from library.models import *
import pyodbc
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=ADMIN;' 
                      'Database=QLTV;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
# Create your views here.
def home_view(request, *args, **kwargs):
    print(request.user)
    return render(request, "index.html", {})

def search_book(request, *args, **kwargs):
    print(request.user)
    return render(request, "searchbook.html", {})

def admin_login(request, *args, **kwargs):
    print(request.user)
    return render(request, "adminlogin.html", {})

def BookAdd(request, *args, **kwargs):
    Book = Books()
    Book.title = request.POST.get('title')
    Book.position = request.POST.get('position')
    Author = Authors()
    Authors.name = request.POST.get('authorname')
    Subject = Subjects()
    Subject.name = request.POST.get('subjectname')
    cursor.execute(f"insert into BOOKS (TITLE, STATE, POSITION) values('{Book.title}',{Book.state},'{Book.position}')")
    cursor.commit()
    cursor.execute(f"insert into AUTHORS values('{Authors.name}')")
    cursor.commit()
    cursor.execute(f"insert into SUBJECTS values('{Subject.name}')")
    cursor.commit()
    last_book_id = [i[0] for i in cursor.execute(f"SELECT TOP 1 BOOK_ID FROM BOOKS ORDER BY BOOK_ID DESC ")][-1]
    last_author_id = [i[0] for i in cursor.execute(f"SELECT TOP 1 AUTHOR_ID FROM AUTHORS ORDER BY BOOK_ID DESC ")][-1]
    last_subject_id = [i[0] for i in cursor.execute(f"SELECT TOP 1 SUBJECT_ID FROM SUBJECTS ORDER BY SUBJECT_ID DESC ")][-1]
        return render(request, "BookAdd.html", {})

def BookDelete(request, *args, **kwargs):
        return render(request, "BookDelete.html", {}) 

def CardAdd(request, *args, **kwargs):
        return render(request, "CardAdd.html", {})

def MemberAdd(request, *args, **kwargs):
        return render(request, "MemberAdd.html", {})