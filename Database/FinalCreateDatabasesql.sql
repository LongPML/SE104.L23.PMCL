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

select * from BOOKS