# Dev: Michael G.
# Date: 3/21/2018 
# Build with: python, django, html, css
# Description:  Simple user login and registration to the Users database

#------------------------------------- IMPORTS --------------------------------------
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from .models import User
import bcrypt
from django.contrib import messages
#------------------------------------------------------------------------------------


# function that renders the index.html page
def renderIndex(request):
    if "user_id" not in request.session:
        request.session['user_id'] = False
    return render(request, 'login_registration/index.html')


# function that takes user form input from a POST request and creates a new user in db
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, errors, extra_tags=tag)
        return redirect('/login_registration')
    else:
        f = request.POST["firstName"]
        l = request.POST["lastName"]
        e = request.POST["email"]
        p = request.POST["password"]
        hp = bcrypt.hashpw( p.encode(), bcrypt.gensalt() )
        User.objects.create(first_name = f, last_name = l, email_address = e, password_hash = hp)
        u = User.objects.filter(email_address = e, password_hash = hp)[0]
        id = u.id   # get the user id of the user just registered
    return redirect("/login_registration/success/{}".format(id))


# function that renders the success page
def renderSuccess(request, id):
    context = {
        # "user": request.session['user_name']
        "user": User.objects.get(id=id)
    }
    return render(request, 'login_registration/success.html', context)


# function that gets user email and password from a POST on login page and checks for valid creds
def login(request):
    e = request.POST["email"]
    p = request.POST['password']
    hp = bcrypt.hashpw( p.encode(), bcrypt.gensalt() )
    # check if username/email and password exist in system
    temp_users = User.objects.filter(email_address = e)
    if len(temp_users) > 0:
        for n in temp_users:
            if (bcrypt.checkpw(p.encode(), n.password_hash.encode())):
                request.session['user_id'] = n.id
                return redirect('/login_registration/success/{}'.format(n.id))  
    else:
        print 'inside else'
        messages.add_message(request, messages.INFO, 'Incorrect email and or password')
        return redirect('/login_registration')


# function to logout a user and redirect to login/register page
def logout(request):
    request.session['user_id'] = False
    return redirect('/login_registration/goodbye')

# function used to render the goodbye exit page
def renderGoodbye(request):
    return render(request, 'login_registration/goodbye.html')
    