from django.urls import path
from .views import *

urlpatterns = [
    path('',index),
    path('user/create',create),
    path('user/login',login),
    path('user/log_out',logout),
    path('books',add_book),
    path('create',create_book),
    path('books/<int:id>',book_info),
    path('books/<int:id>/update',update),
    path('books/<int:id>/delete',delete),
    path('books/<int:id>/fav',add_fav),
    path('books/<int:id>/unfav',remove_fav),

]
