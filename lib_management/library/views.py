from django.shortcuts import render
import library.models
from library.models import *
import pyodbc
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=NHANCSER\ADMIN;' 
                    #   'Server=ADMIN;'
                      'Database=QLTV;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
# Create your views here.
def home_view(request, *args, **kwargs):
    NewBooks = cursor.execute(f"""SELECT top 4 B.BOOK_ID, B.TITLE, B.PATH, A.NAME AUTHOR
                                    FROM BOOKS B 
                                    LEFT JOIN AUTHORS_BOOKS AB 
                                    ON B.BOOK_ID = AB.BOOK_ID LEFT JOIN AUTHORS A ON AB.AUTHOR_ID = A.AUTHOR_ID
                                    ORDER BY B.BOOK_ID DESC""")
    NewBooks = cursor.fetchall()

    PopularBooks = cursor.execute(f"""SELECT B.BOOK_ID, B.TITLE, B.PATH, A.NAME AUTHOR
                                    FROM BOOKS B 
                                    LEFT JOIN AUTHORS_BOOKS AB 
                                    ON B.BOOK_ID = AB.BOOK_ID LEFT JOIN AUTHORS A ON AB.AUTHOR_ID = A.AUTHOR_ID
                                    WHERE B.TITLE IN (
                                        SELECT TOP 4 BB.TITLE
                                        FROM BOOKS BB JOIN BORROWCARDS BCC ON BB.BOOK_ID = BCC.BOOK_ID
                                        WHERE MONTH(BCC.BORROW_DATE) = MONTH(GETDATE())-1 
                                        AND YEAR(BCC.BORROW_DATE) = YEAR(GETDATE())
                                        GROUP BY BB.TITLE
                                        ORDER BY COUNT(BB.TITLE) DESC)""")
    PopularBooks = cursor.fetchall()

    return render(request, "index.html", {'PopularBooks':PopularBooks,'NewBooks':NewBooks})

def admin_home(request, *args, **kwargs):
    if request.method=="GET":
        result = cursor.execute(f"""SELECT B.BOOK_ID, B.TITLE, A.NAME AUTHOR, S.NAME SUBJECT, LC.NAME,B.POSITION, B.STATE, B.PATH
                                    FROM BOOKS B     
                                    left JOIN AUTHORS_BOOKS AB
                                    ON B.BOOK_ID = AB.BOOK_ID left JOIN AUTHORS A
                                    ON AB.AUTHOR_ID  = A.AUTHOR_ID
                                    left JOIN SUBJECTS_BOOKS SB
                                    ON B.BOOK_ID = SB.BOOK_ID left JOIN SUBJECTS S
                                    ON SB.SUBJECT_ID = S.SUBJECT_ID
                                    LEFT JOIN BORROWCARDS BC 
                                    ON BC.BOOK_ID = B.BOOK_ID LEFT JOIN LIBCARDS LC
                                    ON BC.LIBCARD_ID = LC.LIBCARD_ID""")
        result = cursor.fetchall()
    NewBooks = cursor.execute(f"""SELECT top 4 B.BOOK_ID, B.TITLE, B.PATH, A.NAME AUTHOR
                                    FROM BOOKS B 
                                    LEFT JOIN AUTHORS_BOOKS AB 
                                    ON B.BOOK_ID = AB.BOOK_ID LEFT JOIN AUTHORS A ON AB.AUTHOR_ID = A.AUTHOR_ID
                                    ORDER BY B.BOOK_ID DESC""")
    NewBooks = cursor.fetchall()

    PopularBooks = cursor.execute(f"""SELECT B.BOOK_ID, B.TITLE, B.PATH, A.NAME AUTHOR
                                    FROM BOOKS B 
                                    LEFT JOIN AUTHORS_BOOKS AB 
                                    ON B.BOOK_ID = AB.BOOK_ID LEFT JOIN AUTHORS A ON AB.AUTHOR_ID = A.AUTHOR_ID
                                    WHERE B.TITLE IN (
                                        SELECT TOP 4 BB.TITLE
                                        FROM BOOKS BB JOIN BORROWCARDS BCC ON BB.BOOK_ID = BCC.BOOK_ID
                                        WHERE MONTH(BCC.BORROW_DATE) = MONTH(GETDATE())-1 
                                        AND YEAR(BCC.BORROW_DATE) = YEAR(GETDATE())
                                        GROUP BY BB.TITLE
                                        ORDER BY COUNT(BB.TITLE) DESC)""")
    PopularBooks = cursor.fetchall()
    return render(request, "admin-home.html", {'BookInformation':result,'PopularBooks':PopularBooks,'NewBooks':NewBooks})

def BookAdd(request, *args, **kwargs):
    Book = Books()
    Book.title = request.POST.get('title')
    Book.position = request.POST.get('position')
    Book.path = request.POST.get('path')
    Author = Authors()
    Authors.name = request.POST.get('authorname')
    author_names = [i[0] for i in cursor.execute(f"SELECT NAME FROM AUTHORS")]
    Subject = Subjects()
    Subject.name = request.POST.get('subjectname')
    subject_names = [i[0] for i in cursor.execute(f"SELECT NAME FROM SUBJECTS")]
    if Book.title != None and Book.position !=None and Authors.name != None and Subject.name != None and Book.title != "" and Book.position !="" and Authors.name != "" and Subject.name != "":
        if Book.path != None and Book.path != "":
            cursor.execute(f""" insert into BOOKS (TITLE, STATE, POSITION, PATH)
                         values(N'{Book.title}',{Book.state},N'{Book.position}','{Book.path}')""")
            cursor.commit()
        else:
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
        messages.success(request,'Add Book Sucessfully!')
        return redirect('/book/add')
    return render(request, "BookAdd.html", {})


def BookEdit(request, id_b):

    result = cursor.execute(f"""SELECT B.BOOK_ID, B.TITLE, A.NAME AUTHOR, S.NAME SUBJECT, LC.NAME,B.POSITION, B.STATE, B.PATH
                                FROM BOOKS B     
                                JOIN AUTHORS_BOOKS AB
                                ON B.BOOK_ID = AB.BOOK_ID JOIN AUTHORS A
                                ON AB.AUTHOR_ID  = A.AUTHOR_ID
                                JOIN SUBJECTS_BOOKS SB
                                ON B.BOOK_ID = SB.BOOK_ID JOIN SUBJECTS S
                                ON SB.SUBJECT_ID = S.SUBJECT_ID
                                LEFT JOIN BORROWCARDS BC 
                                ON BC.BOOK_ID = B.BOOK_ID LEFT JOIN LIBCARDS LC
                                ON BC.LIBCARD_ID = LC.LIBCARD_ID
                                WHERE B.BOOK_ID = {id_b}""")
    result = cursor.fetchall()
    return render(request, "BookEdit.html", {'BookDetail':result})

def BookUpdate(request):
    bookid = request.POST.get("ID")
    position = request.POST.get("position")
    state = request.POST.get("state")
    path = request.POST.get("path")
    cursor.execute(f"""UPDATE BOOKS SET STATE = {state}, POSITION = '{position}', PATH = '{path}' WHERE BOOK_ID = {bookid}""")
    cursor.commit()
    # return BookEdit(request, bookid)
    return redirect('/bookDetail/')

def CardAdd(request, *args, **kwargs):
    card = Borrowcards()
    card.bookid = request.POST.get('bookid')
    card.libcardid = request.POST.get('libcardid')
    card.borrow_date = request.POST.get('borrow_date')
    card.due_date = request.POST.get('due_date')
    # card.borrow_date = datetime.datetime.strptime(request.POST.get('date'),"%Y-%m-%d").date()
    if card.bookid != None and card.libcardid != None and card.borrow_date != "" and card.due_date != "" and card.bookid != "" and card.libcardid != "":
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
                                           where LC.NAME like N'%{key}%' or BC.BORROWCARD_ID like '%{key}%' or LC.LIBCARD_ID like '%{key}%'""")
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
        # BOOK_ID = [i for i in cursor.execute(f"""SELECT BOOK_ID FROM BORROWCARDS WHERE BORROWCARD_ID = {card.BORROWCARD_ID}""")][0][0]
        BOOK_ID = cursor.execute(f"""SELECT BOOK_ID FROM BORROWCARDS WHERE BORROWCARD_ID = {card.BORROWCARD_ID}""").fetchall()[0][0]
        cursor.execute(f"""UPDATE BOOKS SET STATE = 1 WHERE BOOK_ID = {BOOK_ID}""")
    cursor.commit()

    # return CardEdit(request,card.BORROWCARD_ID)
    return redirect('/cardDetail/')

def MemberAdd(request, *args, **kwargs):
    member = Libcards()
    member.NAME = request.POST.get('name')
    member.AGES = request.POST.get('age')
    member.ADDRESS = request.POST.get('address')
    member.CLASS = request.POST.get('class')
    if member.NAME != None and member.AGES != None and member.ADDRESS != None and member.CLASS != None and member.NAME != "" and member.AGES != "" and member.ADDRESS != "" and member.CLASS != "":
        cursor.execute(f"""insert into LIBCARDS (NAME, AGES, ADDRESS, CLASS) 
                         values(N'{member.NAME}',{member.AGES},N'{member.ADDRESS}',N'{member.CLASS}')""")
        cursor.commit()
        return render(request, "MemberAdd.html", {})
    else:
        return render(request, "MemberAdd.html", {})

def MemberDetail(request):
    if request.method=="POST":
        key = request.POST.get("key")
        search_result = cursor.execute(f"""select * from LIBCARDS
                                           where NAME like '%{key}%' or LIBCARD_ID like '%{key}%'""")
        return render(request, 'MemberDetail.html', {'Libcards':search_result})

    if request.method=="GET":
        result = cursor.execute(f"""select * from LIBCARDS""")
        result = cursor.fetchall()
        return render(request, 'memberDetail.html', {'Libcards':result})


def BookDetail(request):
    index = 0
    if request.method=="POST":
        key = request.POST.get("key")
        if key is not None:
            search_result = cursor.execute(f"""SELECT B.BOOK_ID, B.TITLE, A.NAME AUTHOR, S.NAME SUBJECT, LC.NAME,B.POSITION, B.STATE, B.PATH
                                        FROM BOOKS B     
                                        left JOIN AUTHORS_BOOKS AB
                                        ON B.BOOK_ID = AB.BOOK_ID left JOIN AUTHORS A
                                        ON AB.AUTHOR_ID  = A.AUTHOR_ID
                                        left JOIN SUBJECTS_BOOKS SB
                                        ON B.BOOK_ID = SB.BOOK_ID left JOIN SUBJECTS S
                                        ON SB.SUBJECT_ID = S.SUBJECT_ID
                                        LEFT JOIN BORROWCARDS BC 
                                        ON BC.BOOK_ID = B.BOOK_ID LEFT JOIN LIBCARDS LC
                                        ON BC.LIBCARD_ID = LC.LIBCARD_ID
                                        WHERE B.BOOK_ID LIKE '%{key}%' or A.NAME LIKE N'%{key}%' OR S.NAME LIKE N'%{key}%' or B.TITLE LIKE N'%{key}%'""")
            return render(request, "BookDetail.html", {'BookDetail':search_result})
        else:
            key = request.POST.get("book")
            search_result = cursor.execute(f"""SELECT B.BOOK_ID, B.TITLE, A.NAME AUTHOR, S.NAME SUBJECT, LC.NAME,B.POSITION, B.STATE, B.PATH
                                        FROM BOOKS B     
                                        left JOIN AUTHORS_BOOKS AB
                                        ON B.BOOK_ID = AB.BOOK_ID left JOIN AUTHORS A
                                        ON AB.AUTHOR_ID  = A.AUTHOR_ID
                                        left JOIN SUBJECTS_BOOKS SB
                                        ON B.BOOK_ID = SB.BOOK_ID left JOIN SUBJECTS S
                                        ON SB.SUBJECT_ID = S.SUBJECT_ID
                                        LEFT JOIN BORROWCARDS BC 
                                        ON BC.BOOK_ID = B.BOOK_ID LEFT JOIN LIBCARDS LC
                                        ON BC.LIBCARD_ID = LC.LIBCARD_ID
                                        WHERE B.BOOK_ID LIKE '%{key}%' or A.NAME LIKE N'%{key}%' OR S.NAME LIKE N'%{key}%' or B.TITLE LIKE N'%{key}%'""")
            return render(request, "res_searchbook.html", {'BookDetail':search_result})
    if request.method=="GET":
        result = cursor.execute(f"""SELECT B.BOOK_ID, B.TITLE, A.NAME AUTHOR, S.NAME SUBJECT, LC.NAME,B.POSITION, B.STATE
                                    FROM BOOKS B     
                                    left JOIN AUTHORS_BOOKS AB
                                    ON B.BOOK_ID = AB.BOOK_ID left JOIN AUTHORS A
                                    ON AB.AUTHOR_ID  = A.AUTHOR_ID
                                    left JOIN SUBJECTS_BOOKS SB
                                    ON B.BOOK_ID = SB.BOOK_ID left JOIN SUBJECTS S
                                    ON SB.SUBJECT_ID = S.SUBJECT_ID
                                    LEFT JOIN BORROWCARDS BC 
                                    ON BC.BOOK_ID = B.BOOK_ID LEFT JOIN LIBCARDS LC
                                    ON BC.LIBCARD_ID = LC.LIBCARD_ID""")
        result = cursor.fetchall()
        return render(request, "BookDetail.html", {'BookDetail':result, 'index':index})


def Login(request, *args, **kwargs):
    username = request.POST.get("username")
    password = request.POST.get("password")
    if username != None and password != None:
        try:
            match = cursor.execute(f"""select PASSWORD from ACCOUNT WHERE USERNAME = '{username}'""").fetchall()[0][0]
            if password == match:
                return redirect('/admin')
            else:
                messages.error(request,'Username or password is not correct!')
                return redirect('/login')
        except:
                messages.error(request,'Username or password is not correct!')
                return redirect('/login')
    return render(request, "Login.html", {})

def bookInformation(request, id_b):
    result = cursor.execute(f"""SELECT B.BOOK_ID, B.TITLE, A.NAME AUTHOR, S.NAME SUBJECT, LC.NAME,B.POSITION, B.STATE, B.PATH
                                FROM BOOKS B     
                                JOIN AUTHORS_BOOKS AB
                                ON B.BOOK_ID = AB.BOOK_ID JOIN AUTHORS A
                                ON AB.AUTHOR_ID  = A.AUTHOR_ID
                                JOIN SUBJECTS_BOOKS SB
                                ON B.BOOK_ID = SB.BOOK_ID JOIN SUBJECTS S
                                ON SB.SUBJECT_ID = S.SUBJECT_ID
                                LEFT JOIN BORROWCARDS BC 
                                ON BC.BOOK_ID = B.BOOK_ID LEFT JOIN LIBCARDS LC
                                ON BC.LIBCARD_ID = LC.LIBCARD_ID
                                WHERE B.BOOK_ID = {id_b}""")
    result = cursor.fetchall()
    return render(request, "book_info.html", {'BookInfor':result})

def ADbookInformation(request, id_b):
    result = cursor.execute(f"""SELECT B.BOOK_ID, B.TITLE, A.NAME AUTHOR, S.NAME SUBJECT, LC.NAME,B.POSITION, B.STATE, B.PATH
                                FROM BOOKS B     
                                JOIN AUTHORS_BOOKS AB
                                ON B.BOOK_ID = AB.BOOK_ID JOIN AUTHORS A
                                ON AB.AUTHOR_ID  = A.AUTHOR_ID
                                JOIN SUBJECTS_BOOKS SB
                                ON B.BOOK_ID = SB.BOOK_ID JOIN SUBJECTS S
                                ON SB.SUBJECT_ID = S.SUBJECT_ID
                                LEFT JOIN BORROWCARDS BC 
                                ON BC.BOOK_ID = B.BOOK_ID LEFT JOIN LIBCARDS LC
                                ON BC.LIBCARD_ID = LC.LIBCARD_ID
                                WHERE B.BOOK_ID = {id_b}""")
    result = cursor.fetchall()
    return render(request, "admin-book_info.html", {'BookInfor':result})


def collections(request, *args, **kwargs):
    if request.method=="GET":
        result = cursor.execute(f"""SELECT B.BOOK_ID, B.TITLE, A.NAME AUTHOR, S.NAME SUBJECT,B.POSITION, B.STATE, B.PATH
                                    FROM BOOKS B     
                                    left JOIN AUTHORS_BOOKS AB
                                    ON B.BOOK_ID = AB.BOOK_ID left JOIN AUTHORS A
                                    ON AB.AUTHOR_ID  = A.AUTHOR_ID
                                    left JOIN SUBJECTS_BOOKS SB
                                    ON B.BOOK_ID = SB.BOOK_ID left JOIN SUBJECTS S
                                    ON SB.SUBJECT_ID = S.SUBJECT_ID""")
        result = cursor.fetchall()
        return render(request, "collections.html", {'BookInformation':result})

def ADcollections(request, *args, **kwargs):
    if request.method=="GET":
        result = cursor.execute(f"""SELECT B.BOOK_ID, B.TITLE, A.NAME AUTHOR, S.NAME SUBJECT,B.POSITION, B.STATE, B.PATH
                                    FROM BOOKS B     
                                    left JOIN AUTHORS_BOOKS AB
                                    ON B.BOOK_ID = AB.BOOK_ID left JOIN AUTHORS A
                                    ON AB.AUTHOR_ID  = A.AUTHOR_ID
                                    left JOIN SUBJECTS_BOOKS SB
                                    ON B.BOOK_ID = SB.BOOK_ID left JOIN SUBJECTS S
                                    ON SB.SUBJECT_ID = S.SUBJECT_ID""")
        result = cursor.fetchall()
        return render(request, "admin-collections.html", {'BookInformation':result})

def searchBook(request, *args, **kwargs):
    key = request.POST.get("book")
    if key is not None:
        search_result = cursor.execute(f"""SELECT B.BOOK_ID, B.TITLE, A.NAME AUTHOR, S.NAME SUBJECT, LC.NAME,B.POSITION, B.STATE, B.PATH
                                    FROM BOOKS B     
                                    left JOIN AUTHORS_BOOKS AB
                                    ON B.BOOK_ID = AB.BOOK_ID left JOIN AUTHORS A
                                    ON AB.AUTHOR_ID  = A.AUTHOR_ID
                                    left JOIN SUBJECTS_BOOKS SB
                                    ON B.BOOK_ID = SB.BOOK_ID left JOIN SUBJECTS S
                                    ON SB.SUBJECT_ID = S.SUBJECT_ID
                                    LEFT JOIN BORROWCARDS BC 
                                    ON BC.BOOK_ID = B.BOOK_ID LEFT JOIN LIBCARDS LC
                                    ON BC.LIBCARD_ID = LC.LIBCARD_ID
                                    WHERE B.BOOK_ID LIKE '%{key}%' or A.NAME LIKE N'%{key}%' OR S.NAME LIKE N'%{key}%' or B.TITLE LIKE N'%{key}%'""")
        return render(request, "res_searchbook.html", {'BookDetail':search_result})

def adminSearchBook(request, *args, **kwargs):
    key = request.POST.get("book")
    if key is not None:
        search_result = cursor.execute(f"""SELECT B.BOOK_ID, B.TITLE, A.NAME AUTHOR, S.NAME SUBJECT, LC.NAME,B.POSITION, B.STATE, B.PATH
                                    FROM BOOKS B     
                                    left JOIN AUTHORS_BOOKS AB
                                    ON B.BOOK_ID = AB.BOOK_ID left JOIN AUTHORS A
                                    ON AB.AUTHOR_ID  = A.AUTHOR_ID
                                    left JOIN SUBJECTS_BOOKS SB
                                    ON B.BOOK_ID = SB.BOOK_ID left JOIN SUBJECTS S
                                    ON SB.SUBJECT_ID = S.SUBJECT_ID
                                    LEFT JOIN BORROWCARDS BC 
                                    ON BC.BOOK_ID = B.BOOK_ID LEFT JOIN LIBCARDS LC
                                    ON BC.LIBCARD_ID = LC.LIBCARD_ID
                                    WHERE B.BOOK_ID LIKE '%{key}%' or A.NAME LIKE N'%{key}%' OR S.NAME LIKE N'%{key}%' or B.TITLE LIKE N'%{key}%'""")
        return render(request, "admin-res_searchbook.html", {'BookDetail':search_result})

def interestedAuthor(request, *args, **kwargs):
    InterestedAuthor = cursor.execute(f"""SELECT T1.*, T2.NumOfBorrowing FROM
                                        (SELECT A.NAME AUTHOR, COUNT(A.NAME) NumOfBooks
                                        FROM AUTHORS_BOOKS AB JOIN AUTHORS A ON AB.AUTHOR_ID = A.AUTHOR_ID
                                        GROUP BY A.NAME) T1
                                        JOIN
                                        (SELECT A.NAME,COUNT(A.NAME) AS NumOfBorrowing
                                        FROM AUTHORS_BOOKS AB JOIN AUTHORS A ON AB.AUTHOR_ID = A.AUTHOR_ID
                                        JOIN BOOKS B ON B.BOOK_ID = AB.BOOK_ID
                                        JOIN BORROWCARDS BC ON BC.BOOK_ID = B.BOOK_ID
                                        WHERE MONTH(BC.BORROW_DATE) = MONTH(GETDATE())-1
                                        AND YEAR(BC.BORROW_DATE) = YEAR(GETDATE())
                                        GROUP BY A.NAME) T2
                                        ON T1.AUTHOR = T2.NAME
                                        ORDER BY T2.NumOfBorrowing DESC""")
    if request.method == "POST":
        key = request.POST.get("key")
        InterestedAuthor = cursor.execute(f"""SELECT T1.*, T2.NumOfBorrowing FROM
                                        (SELECT A.NAME AUTHOR, COUNT(A.NAME) NumOfBooks
                                        FROM AUTHORS_BOOKS AB JOIN AUTHORS A ON AB.AUTHOR_ID = A.AUTHOR_ID
                                        GROUP BY A.NAME) T1
                                        JOIN
                                        (SELECT A.NAME,COUNT(A.NAME) AS NumOfBorrowing
                                        FROM AUTHORS_BOOKS AB JOIN AUTHORS A ON AB.AUTHOR_ID = A.AUTHOR_ID
                                        JOIN BOOKS B ON B.BOOK_ID = AB.BOOK_ID
                                        JOIN BORROWCARDS BC ON BC.BOOK_ID = B.BOOK_ID
                                        WHERE MONTH(BC.BORROW_DATE) = MONTH(GETDATE())-1
                                        AND YEAR(BC.BORROW_DATE) = YEAR(GETDATE())
                                        GROUP BY A.NAME) T2
                                        ON T1.AUTHOR = T2.NAME
                                        WHERE T1.AUTHOR LIKE N'%{key}%'
                                        ORDER BY T2.NumOfBorrowing DESC""")
    
    return render(request, "interested_author.html", {'InterestedAuthor':InterestedAuthor})

def interestedTopic(request, *args, **kwargs):
    InterestedTopic = cursor.execute(f"""SELECT T1.*, T2.NumOfBorrowing FROM
                                        (SELECT S.NAME TOPIC, COUNT(S.NAME) NumOfBooks
                                        FROM SUBJECTS_BOOKS SB JOIN SUBJECTS S ON SB.SUBJECT_ID = S.SUBJECT_ID
                                        GROUP BY S.NAME) T1
                                        JOIN
                                        (SELECT S.NAME,COUNT(S.NAME) AS NumOfBorrowing
                                        FROM SUBJECTS_BOOKS SB JOIN SUBJECTS S ON SB.SUBJECT_ID = S.SUBJECT_ID
                                        JOIN BOOKS B ON B.BOOK_ID = SB.BOOK_ID
                                        JOIN BORROWCARDS BC ON BC.BOOK_ID = B.BOOK_ID
                                        WHERE MONTH(BC.BORROW_DATE) = MONTH(GETDATE())-1 
                                        AND YEAR(BC.BORROW_DATE) = YEAR(GETDATE())
                                        GROUP BY S.NAME) T2
                                        ON T1.TOPIC = T2.NAME
                                        ORDER BY T2.NumOfBorrowing DESC""")
    if request.method == "POST":
        key = request.POST.get("key")
        InterestedTopic = cursor.execute(f"""SELECT T1.*, T2.NumOfBorrowing FROM
                                        (SELECT S.NAME TOPIC, COUNT(S.NAME) NumOfBooks
                                        FROM SUBJECTS_BOOKS SB JOIN SUBJECTS S ON SB.SUBJECT_ID = S.SUBJECT_ID
                                        GROUP BY S.NAME) T1
                                        JOIN
                                        (SELECT S.NAME,COUNT(S.NAME) AS NumOfBorrowing
                                        FROM SUBJECTS_BOOKS SB JOIN SUBJECTS S ON SB.SUBJECT_ID = S.SUBJECT_ID
                                        JOIN BOOKS B ON B.BOOK_ID = SB.BOOK_ID
                                        JOIN BORROWCARDS BC ON BC.BOOK_ID = B.BOOK_ID
                                        WHERE MONTH(BC.BORROW_DATE) = MONTH(GETDATE())-1 
                                        AND YEAR(BC.BORROW_DATE) = YEAR(GETDATE())
                                        GROUP BY S.NAME) T2
                                        ON T1.TOPIC = T2.NAME
                                        WHERE T1.TOPIC LIKE N'%{key}%'
                                        ORDER BY T2.NumOfBorrowing DESC""")

    return render(request, "interested_topic.html", {'InterestedTopic':InterestedTopic})