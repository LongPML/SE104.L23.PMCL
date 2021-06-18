from django.shortcuts import render
import library.models
from library.models import *
import pyodbc
import datetime
from django.http import HttpResponse
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
    author_names = [i[0] for i in cursor.execute(f"SELECT NAME FROM AUTHORS")]
    Subject = Subjects()
    Subject.name = request.POST.get('subjectname')
    subject_names = [i[0] for i in cursor.execute(f"SELECT NAME FROM SUBJECTS")]
    if Book.title != None and Book.position !=None and Authors.name != None and Subject.name != None:
        cursor.execute(f"""insert into BOOKS (TITLE, STATE, POSITION)
                         values(N'{Book.title}',{Book.state},N'{Book.position}')""")
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
    else:
        return render(request, "BookAdd.html", {})

def BookDelete(request, *args, **kwargs):
        return render(request, "BookDelete.html", {})

def CardAdd(request, *args, **kwargs):
    card = Borrowcards()
    card.bookid = request.POST.get('bookid')
    card.libcardid = request.POST.get('libcardid')
    card.borrow_date = request.POST.get('borrow_date')
    card.due_date = request.POST.get('due_date')
    # card.borrow_date = datetime.datetime.strptime(request.POST.get('date'),"%Y-%m-%d").date()
    if card.bookid != None and card.libcardid != None and card.borrow_date != "" and card.due_date != "":
        cursor.execute(f"""insert into BORROWCARDS (BOOK_ID, LIBCARD_ID, BORROW_DATE, DUE_DATE, RETURN_DATE)
                         VALUES({card.bookid},{card.libcardid},'{card.borrow_date}','{card.due_date}',{card.return_date})""")
        cursor.commit()
        cursor.execute(f"""update BOOKS set STATE = 0 WHERE BOOK_ID = {card.bookid}""")
        cursor.commit()
        return render(request, "CardAdd.html", {})
    else:
        return render(request, "CardAdd.html", {})

def CardDetail(request, *args, **kwargs):
    if request.method=="POST":
        key = request.POST.get("key")
        search_result = cursor.execute(f"""select BC.BORROWCARD_ID, LC.NAME, B.TITLE , BC.DUE_DATE, BC.RETURN_DATE
                                           from BORROWCARDS BC join LIBCARDS LC 
                                           on BC.LIBCARD_ID = LC.LIBCARD_ID 
                                           join BOOKS B
                                           on BC.BOOK_ID = B.BOOK_ID
                                           where LC.NAME like '%{key}%' or BC.BORROWCARD_ID like '%{key}%' or LC.LIBCARD_ID like '%{key}%'""")
        return render(request, 'CardDetail.html', {'CardDetail':search_result})

    if request.method=="GET":
        result = cursor.execute(f"""select BC.BORROWCARD_ID, LC.NAME, B.TITLE , BC.DUE_DATE, BC.RETURN_DATE
                                   from BORROWCARDS BC join LIBCARDS LC 
                                   on BC.LIBCARD_ID = LC.LIBCARD_ID 
                                   join BOOKS B
                                   on BC.BOOK_ID = B.BOOK_ID""")
        result = cursor.fetchall()
        return render(request, 'CardDetail.html', {'CardDetail':result})

def CardEdit(request, id_bc):

    result = cursor.execute(f"""select BC.BORROWCARD_ID, LC.NAME, B.TITLE , BC.DUE_DATE, BC.RETURN_DATE
                               from BORROWCARDS BC join LIBCARDS LC 
                               on BC.LIBCARD_ID = LC.LIBCARD_ID 
                               join BOOKS B
                               on BC.BOOK_ID = B.BOOK_ID
                               WHERE BC.BORROWCARD_ID = {id_bc}""")
    result = cursor.fetchall()
    result[0][-2] = result[0][-2].strftime("%Y-%m-%d")
    
    if result[0][-1] == None:
        result[0][-1] = ""
    elif result[0][-1] == "1900-01-01":
        result[0][-1] = ""
    else:
        result[0][-1] = result[0][-1].strftime("%Y-%m-%d")
    return render(request, 'CardEdit.html', {'CardDetail':result})

def CardUpdate(request):
    card = library.models.CardDetail()
    card.BORROWCARD_ID = request.POST.get('bc_id')
    card.NAME = request.POST.get('name')
    card.TITLE = request.POST.get('title')
    card.DUE_DATE = request.POST.get('due_date')
    card.RETURN_DATE = request.POST.get('return_date')
    if card.RETURN_DATE=="1900-01-01":
        cursor.execute(f"""UPDATE BORROWCARDS SET RETURN_DATE = NULL WHERE BORROWCARD_ID = {card.BORROWCARD_ID}""")
    else:
        cursor.execute(f"""UPDATE BORROWCARDS SET RETURN_DATE = '{card.RETURN_DATE}' WHERE BORROWCARD_ID = {card.BORROWCARD_ID}""")
        cursor.commit()
        BOOK_ID = [i for i in cursor.execute(f"""SELECT BOOK_ID FROM BORROWCARDS WHERE BORROWCARD_ID = {card.BORROWCARD_ID}""")][0][0]
        cursor.execute(f"""UPDATE BOOKS SET STATE = 1 WHERE BOOK_ID = {BOOK_ID}""")
    cursor.commit()

    return CardEdit(request,card.BORROWCARD_ID)

def MemberAdd(request, *args, **kwargs):
    member = Libcards()
    member.name = request.POST.get('name')
    member.age = request.POST.get('age')
    member.address = request.POST.get('address')
    member.classroom = request.POST.get('class')
    if member.name != None and member.age != None and member.address != None and member.classroom != None:
        cursor.execute(f"""insert into LIBCARDS (NAME, AGES, ADDRESS, CLASS) 
                         values(N'{member.name}',{member.age},N'{member.address}',N'{member.classroom}')""")
        cursor.commit()
        return render(request, "MemberAdd.html", {})
    else:
        return render(request, "MemberAdd.html", {})

def BookDetail(request):

    if request.method=="POST":
        key = request.POST.get("key")
        search_result = cursor.execute(f"""SELECT B.BOOK_ID, B.TITLE, B.POSITION, LC.NAME
                                            FROM BOOKS B LEFT JOIN BORROWCARDS BC ON B.BOOK_ID = BC.BOOK_ID
                                            LEFT JOIN LIBCARDS LC ON LC.LIBCARD_ID = BC.LIBCARD_ID
                                            WHERE B.TITLE LIKE '%{key}%' OR B.BOOK_ID LIKE '%{key}%'""")
        return render(request, "BookDetail.html", {'BookDetail':search_result})

    if request.method=="GET":
        result = cursor.execute(f"""SELECT B.BOOK_ID, B.TITLE, B.POSITION, LC.NAME
                                    FROM BOOKS B LEFT JOIN BORROWCARDS BC ON B.BOOK_ID = BC.BOOK_ID
                                    LEFT JOIN LIBCARDS LC ON LC.LIBCARD_ID = BC.LIBCARD_ID""")
        result = cursor.fetchall()
        return render(request, "BookDetail.html", {'BookDetail':result})


