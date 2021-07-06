CREATE DATABASE QLTV
USE QLTV
create table LIBCARDS(
LIBCARD_ID int IDENTITY(1,1) CONSTRAINT PK_LC PRIMARY KEY,
NAME nVarchar(30)	Not Null,
AGES INT not null,
ADDRESS nVARCHAR(100) NOT NULL,
CLASS nVARCHAR(15) NOT NULL
)

create table BOOKS(
BOOK_ID	int IDENTITY(1,1) CONSTRAINT PK_B PRIMARY KEY,
TITLE	nVarchar(30)	Not Null,
STATE INT not null,
POSITION nVARCHAR(10) not null
)



create table SUBJECTS(
SUBJECT_ID int IDENTITY(1,1) CONSTRAINT PK_SJ PRIMARY KEY,
NAME	nVarchar(30)	Not Null,
)

create table AUTHORS(
AUTHOR_ID int IDENTITY(1,1) CONSTRAINT PK_A PRIMARY KEY,
NAME	nVarchar(30)	Not Null,
)

create table BORROWCARDS(
BORROWCARD_ID int IDENTITY(1,1) CONSTRAINT PK_BC PRIMARY KEY,
BOOK_ID INT NOT NULL CONSTRAINT FK_BC_B  FOREIGN KEY REFERENCES BOOKS(BOOK_ID),
LIBCARD_ID INT NOT NULL CONSTRAINT FK_BC_LC  FOREIGN KEY REFERENCES LIBCARDS(LIBCARD_ID),
BORROW_DATE DATETIME NOT NULL,
DUE_DATE DATETIME NOT NULL,
RETURN_DATE DATETIME NULL
)

CREATE TABLE SUBJECTS_BOOKS(
SUBJECT_ID INT NOT NULL CONSTRAINT FK_SJ_B FOREIGN KEY REFERENCES SUBJECTS(SUBJECT_ID),
BOOK_ID INT NOT NULL CONSTRAINT FK_B_SJ FOREIGN KEY REFERENCES BOOKS(BOOK_ID),
CONSTRAINT PK_SJ_B PRIMARY KEY (SUBJECT_ID,BOOK_ID)
)

CREATE TABLE AUTHORS_BOOKS(
AUTHOR_ID INT NOT NULL CONSTRAINT FK_A_B FOREIGN KEY REFERENCES AUTHORS(AUTHOR_ID),
BOOK_ID INT NOT NULL CONSTRAINT FK_B_A FOREIGN KEY REFERENCES BOOKS(BOOK_ID),
CONSTRAINT PK_A_B PRIMARY KEY (AUTHOR_ID,BOOK_ID)
)

CREATE TABLE ACCOUNT(
	USERNAME VARCHAR(20) CONSTRAINT PK_ACC PRIMARY KEY,
	PASSWORD VARCHAR(30)
)
INSERT INTO ACCOUNT VALUES('ADMIN','ADMIN')

ALTER TABLE BOOKS ADD PATH NVARCHAR(200) NULL
ALTER TABLE BOOKS ALTER COLUMN TITLE nVarchar(50)

SET DATEFORMAT dmy

--use QLTV EXEC sp_changedbowner 'sa' --dung de cap quyen owner cho database de ve diagram khi copy tu may nay qua may khac

select * from AUTHORS_BOOKS

SELECT T1.*, T2.NumOfBorrowing FROM
                                        (SELECT A.NAME AUTHOR, COUNT(A.NAME) NumOfBooks, AB.BOOK_ID
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

                                        --JOIN BOOKS B 
                                        --ON B.BOOK_ID = T2.BOOK_ID LEFT JOIN AUTHORS A ON T2.AUTHOR_ID = A.AUTHOR_ID
                                        --WHERE B.TITLE IN (
                                        --SELECT TOP 1 BB.TITLE
                                        --FROM BOOKS BB JOIN BORROWCARDS BCC ON BB.BOOK_ID = BCC.BOOK_ID
                                        --WHERE MONTH(BCC.BORROW_DATE) = MONTH(GETDATE())-1 
                                        --AND YEAR(BCC.BORROW_DATE) = YEAR(GETDATE())
                                        --GROUP BY BB.TITLE
                                        --ORDER BY COUNT(BB.TITLE) DESC)

                                        ORDER BY T2.NumOfBorrowing DESC