from django.shortcuts import render,redirect
from django.http import HttpRequest
from .models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="/login/")
def homepage(request):
    return render(request,"pages/home.html")

@login_required(login_url="/login/")
def add_recipe(request):
    if request.method == "POST":
       data = request.POST
       name = data.get('recipe_name')
       description = data.get('recipe_description')
       image = request.FILES.get('recipe_image')
       print(request.user.id)
      # print(name)
      # print(description)
      # print(image)
       Recipe.objects.create(name = name , description = description , image = image , user_id = request.user.id)

       return redirect('/add-recipe/') 


    return render(request, "pages/add_recipe.html",context={'page_name' : "Add-recipe"})

@login_required(login_url="/login/")
def view_all(request):
    id = request.user.id
    recipe_set = Recipe.objects.filter(user_id = id)
    return render(request,"pages/view_all.html",context={'recipe_set':recipe_set , 'page_name' : "View-all"})

@login_required(login_url="/login/")
def delete_recipe(request):
    if request.method == "POST":
        data = request.POST
        #print(data)
        input_name = data.get('recipe_name')
        print(input_name)
        recipe_set = Recipe.objects.all()
        is_found = False
        for x in recipe_set:
            print(x.name)
            print(x.id)
            if(x.name == input_name):
                Recipe.objects.filter(id = x.id).delete()
        return redirect('/delete-recipe/')   

    return render(request,"pages/delete_recipe.html")

@login_required(login_url="/login/")
def delete_select(request):
    id = request.user.id
    recipe_set = Recipe.objects.filter(user_id = id)
    return render(request,"pages/delete-select.html",context={'recipe_set' : recipe_set})

@login_required(login_url="/login/")
def delete_id(request,id):
    Recipe.objects.filter(id = id).delete()
    return redirect('/delete-select/')

@login_required(login_url="/login/")
def search(request):
    id = request.user.id
    is_found = False
    recipe_found = None  # Initialize recipe_found variable
    
    if request.method == "POST":
        data = request.POST
        input_name = data.get('recipe_name')
        recipe_set = Recipe.objects.filter(user_id = id)
        
        for x in recipe_set:    
            if x.name == input_name:
                is_found = True
                ans_name = x.name
                ans_desc = x.description
                ans_image = x.image
                break  # Break out of the loop once a match is found

    
    if is_found:
        return render(request, "pages/search.html", context={'ans_name': ans_name,'ans_desc': ans_desc,'ans_image': ans_image ,'found': True})
    else:
        return render(request, "pages/search.html", context={'answer': "Recipe not found", 'found': False})

@login_required(login_url="/login/")
def update(request):
    id = request.user.id
    recipe_set = Recipe.objects.filter(user_id = id)
    return render(request,'pages/update.html',context={'recipe_set' : recipe_set})

@login_required(login_url="/login/")
def update_id(request,id):
    update_recipe = Recipe.objects.get(id = id)
    if request.method == "POST":

        data = request.POST
        name = data.get('recipe_name')
        description = data.get('recipe_description')
        image = request.FILES.get('recipe_image')        
        
        update_recipe.name = name
        update_recipe.description = description
        
        if image:
            update_recipe.image = image
        
        update_recipe.save()
        return redirect('/#/')
    return render(request,'pages/update-id.html',context = {'update_recipe' : update_recipe})    

def login_page(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        if not User.objects.filter(username = username).exists():
            messages.error(request, "Incorrect username")
            return redirect('/login/')
        # to check password
        u1 = authenticate(username = username, password = password)
        if u1 is None:
            messages.error(request, "Incorrect Password")
            return redirect('/login/') 

        login(request,u1)
        return redirect('/#/')

                            

    return render(request,"pages/login.html")

@login_required(login_url="/login/")
def logout_page(request):
    logout(request)
    return redirect('/login/')

def register(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        username = data.get('username')

        #checking if the username has already been taken or not as username is our primary key for Users
        if User.objects.filter(username = username).exists():
            messages.error(request, "Username has already been taken! Try a different one.")
            return redirect('/register/')

        u1 = User(first_name = first_name , last_name = last_name , email = email , username = username)
        u1.set_password(data.get('password'))
        u1.save()
        messages.success(request, "Registration confirmed!")

        
    return render(request,"pages/register.html")