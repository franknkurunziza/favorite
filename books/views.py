from .models import User, Book
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'register.html')

def create(request):
    errors=User.objects.user_valid(request.POST)

    if len(errors)>0:
        for key , value in errors.items():
            messages.error(request,value, extra_tags=key)
        return redirect('/')

    hashed_pw=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    user1=User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hashed_pw,
    )
    request.session['log_user_id']=user1.id
    request.session['user_firstname']=user1.first_name
    request.session['user_lastname']=user1.last_name

    return redirect('/books')


def login(request):
    if request.method== 'POST':
        user_list = User.objects.filter(email=request.POST['email'])

        if user_list:
            logged_user = user_list[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['log_user_id'] = logged_user.id
                request.session['user_firstname']=logged_user.first_name
                request.session['user_lastname']=logged_user.last_name
                return redirect('/books')
            else:
                messages.error(request, "Invalid email or password", extra_tags='not_found')
                return redirect('/')
        messages.error(request, "Email Not Found", extra_tags='not_found')
        return redirect('/')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def add_book(request):
    if 'log_user_id' not in request.session:
        return redirect('/')

    context={
        'user': User.objects.get(id=request.session['log_user_id']),
        'books':Book.objects.all()
    }

    return render(request,'book.html',context)

def create_book(request):
    if 'log_user_id' not in request.session:
        return redirect('/')

    errors=Book.objects.book_valid(request.POST)

    if len(errors)>0:
        for key , value in errors.items():
            messages.error(request,value, extra_tags=key)
        return redirect('/books')
    book1=Book.objects.create(
        title=request.POST['title'],
        desc=request.POST['desc'],
        uploaded_by=User.objects.get(id=request.session['log_user_id'])
    )

    user=User.objects.get(id=request.session['log_user_id'])
    book1.users_who_like.add(user)

    request.session['book_id']=book1.id

    return redirect('/books')

def book_info(request,id):
    if 'log_user_id' not in request.session:
        return redirect('/')

    book=Book.objects.get(id=id)
    context={
        'book_info':book,
        'user_log':User.objects.get(id=request.session['log_user_id'])
        

    }
    if request.session['log_user_id'] == book.uploaded_by.id:
        return render(request,'book_edit.html', context)
    else:
        return render(request,'book_desc.html',context)

def update(request,id):
    errors=Book.objects.book_valid(request.POST)
    book=Book.objects.get(id=id)

    if len(errors)>0:
        for key , value in errors.items():
            messages.error(request,value, extra_tags=key)
        return redirect(f'/books/{book.id}')

    book.title=request.POST['title']
    book.desc=request.POST['desc']
    book.save()
    return redirect(f'/books')

def delete(request,id):
    book=Book.objects.get(id=id)
    book.delete()
    return redirect('/books')

def add_fav(request,id):
    book=Book.objects.get(id=id)
    user=User.objects.get(id=request.session['log_user_id'])
    user.liked_books.add(book)
    return redirect(f'/books/{book.id}')

def remove_fav(request,id):
    book=Book.objects.get(id=id)
    user=User.objects.get(id=request.session['log_user_id'])
    book.users_who_like.remove(user)
    return redirect(f'/books/{book.id}')


# Create your views here.
