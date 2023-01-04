
from multiprocessing import context
from django.contrib import messages
from django.views import generic
from django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from youtubesearchpython import Video,VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'home.html')

###########start books##########################
@login_required
def books(request):
    form = DashboardForm()
    
    context = {
        'form':form 
        
    }
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
                
            }
            result_list.append(result_dict) 
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'books.html',context)       
    else:
        form = DashboardForm()
    
    
    return render(request,'books.html',context)



############# end books ####################


def login(request):
    return render(request,'login.html')

def logout(request):
    return render(request,'logout.html')

def register(request):
    if request.method == 'POST':
        form  = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Created for {username}!")
            return redirect('login')
    else:
        form  = UserRegisterForm()
    context = {
        'form':form
    }
    
    return render(request,'register.html',context)

#############start todo##################
@login_required
def todo(request):
    todo = Todo.objects.filter(user=request.user)
    form = TodoForm()
    
    if len(todo) == 0:
        todo_done= True
    else:
        todo_done=False
    
    context = {
        'todo':todo,
        'form':form,
        'todo_done':todo_done
    }
    
    if request.method=='POST':
        to = TodoForm(request.POST)
        if to.is_valid():
            try:
                finished =request.POST['Status']
                if finished =='on':
                    finished=True
                else:
                    finished=False    
                
            except:    
                finished =False
                
            to = Todo(user=request.user,Title=request.POST['Title'],Status=finished)
            to.save()
            messages.success(request,f"todo Addes from successfully!")
            return redirect("todo")
        
    
    
    
    return render(request,'todo.html',context)
 
@login_required    
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")

@login_required
def update_todo(request,pk=None):
    to = Todo.objects.get(id=pk)
    if to.Status ==False:
        to.Status=True
        
    elif to.Status ==True:
       to.Status=False    
    
    else:
        to.Status = True
    to.save()  
          
    return redirect("todo")


#######end todo ######################


###########start wiki###################
@login_required
def wiki(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = str(request.POST['text'])
        search = wikipedia.page(text)
        if search:
            context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary,
            }
            return render(request,'wiki.html',context)
        else:    
             form = DashboardForm()
             context={
            'form':form
            }
    else:    
        form = DashboardForm()
        context={
        'form':form
        }
    return render(request,'wiki.html',context)

##################end###############################

##########start conv##########
@login_required
def conversion(request):
    if request.method =='POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'me_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first =  request.POST['measure1']
                second =  request.POST['measure2']
                input =  request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot' 
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'    
                context = {
                    'form':form,
                    'me_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'me_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first =  request.POST['measure1']
                second =  request.POST['measure2']
                input =  request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram' 
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)/2.20462} pound'    
                context = {
                    'form':form,
                    'me_form':measurement_form,
                    'input':True,
                    'answer':answer
                }    
    else:    
        form = ConversionForm()
        context = {
        'form':form,
        'input':False
        }
    return render(request,'conversion.html',context)
##########end conv##########



##############start dic########################
@login_required
def dictionary(request):
    
    if request.method =='POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            
            context={
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms': synonyms
            }
        except:
            context={
                'form':form,
                'input':'',
            }
        return render(request,'dictionary.html',context)        
    else:
         form = DashboardForm()
         context={'form':form }
           
    return render(request,'dictionary.html',context)



############end#############################

##############start homework##############################
@login_required
def homework(request):
    homework = HomeWork.objects.filter(user=request.user)
    if len(homework)==0:
        homework_done= True
    else:
        homework_done=False    
        
    context = {
        'Homework':homework,
        'form':  HomeForm()
    }
    
    if request.method == 'POST':
        hw = HomeForm(request.POST)
        if hw.is_valid():
            try:
                finished =request.POST['Status']
                if finished =='on':
                    finished=True
                else:
                    finished=False    
                
            except:    
                finished =False
                
            hw = HomeWork(user=request.user,Subject=request.POST['Subject'],Title=request.POST['Title'],Description=request.POST['Description'],Due=request.POST['Due'],Status=finished)
            hw.save()
            messages.success(request,f"Homework Addes from {request.user.username} successfully!")
            return redirect("homework")
    else:
        form = HomeForm()
    return render(request,'homework.html',context)

@login_required

def delete_homework(request,pk=None):
    HomeWork.objects.get(id=pk).delete()
    return redirect("homework")
@login_required
def update_homework(request,pk=None):
    home = HomeWork.objects.get(id=pk)
    if home.Status ==False:
        home.Status=True
        
    elif home.Status ==True:
        home.Status=False    
    
    else:
        home.Status = True
    home.save()  
          
    return redirect("homework")
##############end########################################

############# start notes#############################
@login_required
def notes_detail(request,pk):
    notes = get_object_or_404(Note,id=pk)
    
    context = {
        'notes':notes
    }
    return render(request,'notes_detail.html',context)

@login_required
def notes(request):
    context = {
        'notes': Note.objects.filter(user=request.user),
        'form':  NotesForm()
        
    }
    if request.method == 'POST':
        note = NotesForm(request.POST)
        if note.is_valid():
            notes = Note(user=request.user,Title=request.POST['Title'],Description=request.POST['Description'])
            notes.save()
        messages.success(request,f"notes Addes from {request.user.username} successfully!")    
        return redirect("notes")
    else:
        note=NotesForm()
    
    
    return render(request,'notes.html',context)

@login_required
def delete_notes(request,pk=None):
    Note.objects.get(id=pk).delete()
    return redirect("notes")
################################################






#########start yoytube #########################
@login_required
def youtube(request):
    context = {
        'form': DashboardForm()
        
    }
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=10000055295965960)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'duration':i['duration'],
                'thumbnails':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'title':i['title'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
                
            }
            desc=""
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text'] 
            result_dict['description'] = desc
            result_list.append(result_dict) 
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'youtube.html',context)       
    else:
        form = DashboardForm()
        
    return render(request,'youtube.html',context)
#######end################

def Delete_homework(request , id):
    delete_book = get_object_or_404(HomeWork , id= id)
    if request.method == 'POST':
        delete_book.delete()
        messages.success(request,f"homework delete from {request.user.username} successfully!")
        return redirect('homework')
    
    context = {
        'delete': HomeWork.objects.all(),
        
    }
    return render(request , 'delete.html',context)

def Delete_todo(request , id):
    delete_book = get_object_or_404(Todo , id= id)
    if request.method == 'POST':
        delete_book.delete()
        messages.success(request,f"todo delete from {request.user.username} successfully!")
        return redirect('todo')
    
    context = {
        'delete':Todo.objects.all(),
        
    }
    return render(request , 'delete.html',context)

def Delete_notes(request , id):
    delete_book = get_object_or_404(Note , id= id)
    if request.method == 'POST':
        delete_book.delete()
        messages.success(request,f"notes delete from {request.user.username} successfully!") 
        return redirect('notes')
    
    context = {
        'delete': Note.objects.all(),
        
    }
    return render(request , 'delete.html',context)
