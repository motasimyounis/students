from re import template
from django.urls import path
from . import views
from django.urls import reverse
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.index,name="index"),
    path('books/',views.books,name="books"),
    path('conversion/',views.conversion,name="conversion"),
    path('dictionary/',views.dictionary,name="dictionary"),
    path('homework/',views.homework,name="homework"),
    path('delete_homework/<int:pk>/',views.delete_homework,name="delete-homework"),
    path('update_homework/<int:pk>/',views.update_homework,name="update-homework"),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name="logout"),
    path('register/',views.register,name="register"),
    path('notes/',views.notes,name="notes"),
    path('delete_note/<int:pk>/',views.delete_notes,name="delete-note"),
    path('notes_detail/<int:pk>/',views.notes_detail,name="notes-detail"),
    path('todo/',views.todo,name="todo"),
    path('delete_todo/<int:pk>/',views.delete_todo,name="delete-todo"),
    path('update_todo/<int:pk>/',views.update_todo,name="update-todo"),
    path('wiki/',views.wiki,name="wiki"),
    path('youtube/',views.youtube,name="youtube"),
    path('delete_notes/<int:id>',views.Delete_notes,name='delete-notes' ),
    path('delete_homework/<int:id>',views.Delete_homework,name='delete-homeworks' ),
    path('delete_todo/<int:id>',views.Delete_todo,name='delete-todos' ),    
               
]
