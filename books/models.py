from django.db import models

import re

class UserManager(models.Manager):
    def user_valid(self,postData):
        errors={}
        Email_Reg=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        users = User.objects.filter(email=postData['email'])

        # Name_reg=re.compile(r'^[a-zA-Z0-9]+$')
        # Pass_Reg=re.compile(r'^[a-zA-Z]+$')

        if len(postData['first_name'])<2:
            errors['first_name']='FirstName can note be less than 2 character'

        if len(postData['last_name'])<2:
            errors['last_name']='LastName can note be less than 2 character'

        if not Email_Reg.match(postData['email']):
            errors['email']='Invalid Email adress!'

        if users:
            errors['unique']='Email already Exist'

        if len(postData['password']) < 8 :
            errors['p_short']='Password should be 8 characters'

        # if not Pass_Reg.match(postData['password']):
        #     errors['only']='Use only string'

        if postData['password'] != postData['conf_password']:
            errors['password']='Invalid Passsword or Mismatch '

        
        return errors 


class BookManager(models.Manager):
    def book_valid(self,postData):
        errors={}
        book_title = Book.objects.filter(title=postData['title'])
        
        if len(postData['title'])<1:
            errors['title']='The Title is required'

        if len(postData['desc']) < 5 :
            errors['desc']='Description have to at least five characters'

        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField()
    password=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    # liked_books=all 


class Book(models.Model):
    title=models.CharField(max_length=255)
    desc=models.TextField()
    uploaded_by=models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like=models.ManyToManyField(User, related_name="liked_books")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=BookManager()

# Create your models here.
