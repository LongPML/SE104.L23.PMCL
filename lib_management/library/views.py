from django.shortcuts import render
from library.models import *
import pyodbc
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=ADMIN;' 
                      'Database=QLTV2;'
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
    author_names = [i[0] for i in cursor.execute(f"SELECT NAME FROM AUTHORS")]
    Subject = Subjects()
    Subject.name = request.POST.get('subjectname')
    subject_names = [i[0] for i in cursor.execute(f"SELECT NAME FROM SUBJECTS")]
    cursor.execute(f"insert into BOOKS (TITLE, STATE, POSITION) values(N'{Book.title}',{Book.state},N'{Book.position}')")
    cursor.commit()
    if Authors.name not in author_names:
        cursor.execute(f"insert into AUTHORS values(N'{Authors.name}')")
        cursor.commit()
    if Subject.name not in subject_names:
        cursor.execute(f"insert into SUBJECTS values(N'{Subject.name}')")
        cursor.commit()
    last_book_id = [i[0] for i in cursor.execute(f"SELECT BOOK_ID FROM BOOKS WHERE TITLE = N'{Book.title}' ")][-1]
    last_author_id = [i[0] for i in cursor.execute(f"SELECT AUTHOR_ID FROM AUTHORS WHERE NAME = N'{Authors.name}' ")][-1]
    last_subject_id = [i[0] for i in cursor.execute(f"SELECT SUBJECT_ID FROM SUBJECTS WHERE NAME = N'{Subject.name}' ")][-1]
    cursor.execute(f"insert into AUTHORS_BOOKS values({last_author_id},{last_book_id})")
    cursor.commit()
    cursor.execute(f"insert into SUBJECTS_BOOKS values({last_subject_id},{last_book_id})")
    cursor.commit()
    return render(request, "BookAdd.html", {})

def BookDelete(request, *args, **kwargs):
        return render(request, "BookDelete.html", {})

def CardAdd(request, *args, **kwargs):
        return render(request, "CardAdd.html", {})

def MemberAdd(request, *args, **kwargs):
        return render(request, "MemberAdd.html", {})