from django.shortcuts import render, redirect
from .models import Restaurant
from .forms import RestaurantForm, SignupForm, SigninForm
from django.contrib.auth import login, logout, authenticate

def signup(request):
    my_form = SignupForm()
    if request.method == "POST":
        my_form = SignupForm(request.POST)
        if my_form.is_valid():
            user_obj = my_form.save(commit=False)
            user_obj.set_password(user_obj.password)
            user_obj.save()
            login(request, user_obj)
            return redirect('restaurant-list')
    
    context = {
        "form": my_form
    }
    
    return render(request, 'signup.html', context)

def signin(request):
    my_form = SigninForm()
    if request.method == "POST":
        my_form = SigninForm(request.POST)
        if my_form.is_valid():
            input_username = my_form.cleaned_data['username']
            input_password = my_form.cleaned_data['password']
            user_obj = authenticate(username=input_username, password=input_password) 
            if user_obj is not None:
                login(request, user_obj)
                return redirect('restaurant-list')
    context = {
        "form": my_form
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect('signin')
    

def restaurant_list(request):
    context = {
        "restaurants":Restaurant.objects.all()
    }
    return render(request, 'list.html', context)


def restaurant_detail(request, restaurant_id):
    context = {
        "restaurant": Restaurant.objects.get(id=restaurant_id)
    }
    return render(request, 'detail.html', context)

def restaurant_create(request):
    form = RestaurantForm()
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('restaurant-list')
    context = {
        "form":form,
    }
    return render(request, 'create.html', context)

def restaurant_update(request, restaurant_id):
    restaurant_obj = Restaurant.objects.get(id=restaurant_id)
    form = RestaurantForm(instance=restaurant_obj)
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant_obj)
        if form.is_valid():
            form.save()
            return redirect('restaurant-list')
    context = {
        "restaurant_obj": restaurant_obj,
        "form":form,
    }
    return render(request, 'update.html', context)

def restaurant_delete(request, restaurant_id):
    restaurant_obj = Restaurant.objects.get(id=restaurant_id)
    restaurant_obj.delete()
    return redirect('restaurant-list')
