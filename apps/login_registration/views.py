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


def renderIndex(request):
    return render(request, 'login_registration/index.html')


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
        # getting user name and placing in a session to use in render below
        f_name = u.first_name
        l_name = u.last_name
        full_name = f_name + ' ' + l_name
        request.session['user_name'] = full_name
        id = u.id
    return redirect("/login_registration/success/{}".format(id))


def renderSuccess(request, id):
    context = {
        "user": request.session['user_name']
    }
    return render(request, 'login_registration/success.html', context)


def login(request):
    e = request.POST["email"]
    p = request.POST['password']
    hp = bcrypt.hashpw( p.encode(), bcrypt.gensalt() )
    # check if username/email and password exist in system
    temp_users = User.objects.filter(email_address = e)
    if len(temp_users) > 0:
        for n in temp_users:
            if (bcrypt.checkpw(p.encode(), n.password_hash.encode())):
                f_name = n.first_name
                l_name = n.last_name
                full_name = f_name + ' ' + l_name
                request.session['user_name'] = full_name
                id = n.id
                return redirect('/login_registration/success/{}'.format(n.id))  
    else:
        messages.add_message(request, messages.INFO, 'Incorrect email and or password')
        return redirect('/login_registration')


# def edit(request, id):
#     context = {
#         "data": User.objects.get( id=id ),
#         "flag": 1
#     }
#     print context['data'].first_name
#     print context['data']
#     print context['flag']
#     return render(request, "restful_users/newUser.html", context)


# def update(request, id):
#     print id
#     errors = User.objects.basic_validator(request.POST)
#     if len(errors):
#         for tag, error in errors.iteritems():
#             messages.error(request, error, extra_tags=tag)
#         return redirect( '/users/{}/edit/'.format(id) )
#     else:
#         U = User.objects.get(id = id)
#         U.first_name = request.POST['firstName']
#         U.last_name = request.POST['lastName']
#         U.email = request.POST['email']
#         U.save()
#     return redirect('/users')


# def show(request, id):
#     context = {
#         "data": User.objects.get(id=id)
#     }
#     return render(request, 'restful_users/user.html', context)


# def delete(request, id):
#     print id
#     u = User.objects.get(id=id)
#     print u
#     u.delete()
#     return redirect('/users')
