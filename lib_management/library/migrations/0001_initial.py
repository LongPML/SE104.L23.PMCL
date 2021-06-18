# Generated by Django 3.2.4 on 2021-06-17 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('position', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Borrowcards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookid', models.IntegerField()),
                ('libcardid', models.IntegerField()),
                ('borrow_date', models.DateField(auto_now=True)),
                ('due_date', models.DateField()),
                ('return_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='CardDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_card', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=30)),
                ('due_date', models.DateField()),
                ('return_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Libcards',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('address', models.CharField(max_length=100)),
                ('classoom', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
    ]