
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login
from .forms import UserRegistrationForm
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from pymongo import MongoClient
from datetime import datetime
import json

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            groups = form.cleaned_data.get('groups')
            if groups:
                for group in groups:
                    user.groups.add(group)
                    groupname= group
            #mongodb
            update = datetime.now()
            client = MongoClient(host='localhost', port=27017)  
            db =client['sparky']
            data = {
                    'username': username,
                    'email': email,
                    'department': str(groupname),
                    'update':update.strftime("%Y-%m-%d %H:%M:%S")
                }
            db.user_details.insert_one(data)
            client.close()
            messages.success(request, 'Registration successful.')
            return redirect('register')
        else:
            messages.success(request, 'User name already Exists')
            return redirect('register')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password') 
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if "admin" in str(user).lower():
                    response = redirect('admin_login')
                    response.set_cookie('username', username) 
                    return response
                else:
                    response = redirect('DEP_1')
                    response.set_cookie('username', username) 
                    return response
            else:
                messages.warning(request, 'Please Check username and password')
                print("Authentication failed. Invalid username or password.")
    except Group.DoesNotExist:
        messages.warning(request, 'Please Create Group first')
    except Exception as e:
        print('error',e)
    return render(request, 'login.html')

def admin_login(request):
    if 'username' in request.COOKIES and request.COOKIES['username'] == 'admin':
        client = MongoClient(host='localhost', port=27017)  
        db = client['sparky']
        task = db['task_details'].find()
        task_list = list(task)
        return render(request, 'admin.html', {'task': task_list})
    else:
        messages.warning(request, 'Only allow admin')
        return redirect('home')

def task_assign(request):
    user = request.user
    if user.is_authenticated:
        username = user.get_username()
    client = MongoClient(host='localhost', port=27017)  
    db =client['sparky']
    dep = db['user_details'].find()
    list_dep = list(dep)
    db2 = client['user_data']
    dep2 = db2['auth_group'].find()
    dep2_list = list(dep2)

    content = {'dep':list_dep,'dep2':dep2_list}
    if request.method == "POST":
        depart = request.POST.get('depart')
        user_name = request.POST.get('user') 
        task = request.POST.get('task') 
        #database update
        highest_token = db.task_details.find_one(sort=[("ticket", -1)]) 
        next_token = 1 
        if highest_token:
            next_token = highest_token['ticket'] + 1  

        update = datetime.now()
        data = {
            'depart': depart,
            'username': user_name,
            'task': task,
            'ticket': next_token,
            'update':update.strftime("%Y-%m-%d %H:%M:%S")
        }
        db.task_details.insert_one(data)
        client.close()
        messages.success(request, 'Task Successfully created.')
    return render(request,'task_assign.html',content)

def logout_user(request):
    logout(request)
    request.session.flush()  
    # Clearing all cookies
    response = redirect('home')
    response.delete_cookie('username') 
    return response

def DEP_1(request):
    username = request.COOKIES.get('username')
    client = MongoClient(host='localhost', port=27017)  
    db = client['sparky']
    task = db['task_details'].find({'username':username})
    task_list = list(task)
    return render(request, 'Deparment.html', {'task': task_list,'user':username})

def update(request, num):
    username = request.COOKIES.get('username')
    client = MongoClient(host='localhost', port=27017)  
    db = client['sparky']
    task = db['task_details'].find({'ticket':num})
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if task:
        task_list = list(task)
    else:
        messages.warning(request, 'No Data')
    if request.method == "POST":
        task_collection = db['task_details']
        update = request.POST.get('user_update')
        remark = request.POST.get('remark')
        task_collection.update_one({'ticket': num}, {'$set': {'status': update,'remark': remark,'user_update':time}}, upsert=True)
        client.close()
        return redirect('DEP_1')
    return render(request, 'update.html', {'task': task_list})

def sum(request, num):
    your = num+20
    return HttpResponse(your)


def welcome(request, num, name):
    print('num',num)
    return HttpResponse("hi " + str(name) + ", your salary "+str(num) )

