# Dev: Michael G.
# Date: 3/21/2018 
# Build with: python, django, html, css
# Description:  trip sharing application that stores and displays users upcoming trips
# and allows others to view and join their trips

#------------------------------------- IMPORTS --------------------------------------
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from .models import User, Quote
import bcrypt
from django.contrib import messages
#------------------------------------------------------------------------------------


# function that renders the login page
def renderMain(request):
    if "user_id" not in request.session:
        request.session['user_id'] = False
    return render(request, 'quotes/main.html')


# function that takes user form input from a POST request and creates a new user in db
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, errors, extra_tags=tag)
        return redirect('/main')
    else:
        f = request.POST["firstName"]
        l = request.POST["lastName"]
        a = request.POST['alias']
        e = request.POST["email"]
        p = request.POST["password"]
        d = request.POST['dob']
        hp = bcrypt.hashpw( p.encode(), bcrypt.gensalt() )
        User.objects.create(first_name = f, last_name = l, alias = a, email = e, password_hash = hp, dob = d)
        u = User.objects.filter(email = e, password_hash = hp)[0]
        id = u.id   # get the user id of the user just registered
        request.session['user_id'] = id
    return redirect("/quotes")


# function that renders the trips.html page
def renderQuotes(request):
    #if the user_id is not in the session cookies were lost, redirect to the main login page
    if "user_id" not in request.session:
        return redirect('/main')

    u = User.objects.get(id = request.session['user_id'])
    all_quotes_except_users_fav = Quote.objects.exclude(likedBy = u.id)
    print all_quotes_except_users_fav
    users_favQuote = u.favoriteQuotes.all()

    # myList = []
    # other_users = User.objects.exclude(id=u.id)
    # include = True
    # for person in other_users:
    #     name = person.first_name + " " + person.last_name
    #     person_trips = person.trips.all()
    #     for t in person_trips:
    #         going = t.attendee.all()
    #         if len(going) > 0:
    #             for p in going:
    #                 if p.id == u.id:
    #                     include = False
    #         if include:
    #             myList.append( (name, t) )
    #             include = True

    context = {
        "u": User.objects.get(id = request.session['user_id']),
        "data_1": Quote.objects.exclude(likedBy = u.id),
        "data_2": u.favoriteQuotes.all(),
        # "data_2": Trip.objects.exclude(planner=u.id).exclude(attendee=u.id)
    }
    return render(request, 'quotes/quotes.html', context)


# function that gets user email and password from a POST on login page and checks for valid creds
def login(request):
    #if the user_id is not in the session cookies were lost, redirect to the main login page
    if "user_id" not in request.session:
        return redirect('/main')
    e = request.POST["email"]
    p = request.POST['password']
    hp = bcrypt.hashpw( p.encode(), bcrypt.gensalt() )
    # check if username/email and password exist in system
    temp_users = User.objects.filter(email = e)
    if len(temp_users) > 0:
        for n in temp_users:
            if (bcrypt.checkpw(p.encode(), n.password_hash.encode())):
                request.session['user_id'] = n.id
                return redirect('/quotes') 
            else:
                # print 'inside else'
                messages.add_message(request, messages.INFO, 'Incorrect email and or password')
                return redirect('/main')
    return redirect('/main')


# function that adds a quote to users favs
def add(request, id):
    #if the user_id is not in the session cookies were lost, redirect to the main login page
    if "user_id" not in request.session:
        return redirect('/main')
    u_id = request.session['user_id']
    u = User.objects.get(id=u_id)
    q = Quote.objects.get(id=id)
    u.favoriteQuotes.add(q)
    return redirect('/quotes')


# function that removes a quote from a users fav
def remove(request, id):
    #if the user_id is not in the session cookies were lost, redirect to the main login page
    if "user_id" not in request.session:
        return redirect('/main')
    u_id = request.session['user_id']
    u = User.objects.get(id=u_id)
    q = Quote.objects.get(id=id)
    u.favoriteQuotes.remove(q)
    return redirect('/quotes')

def renderdetails(request, id):
    if "user_id" not in request.session:
        return redirect('/main')
    
    u = User.objects.get(id = id)
    print u.first_name
    qoutes_by_this_user = Quote.objects.filter(postedby = u)
    counter = 0
    for i in qoutes_by_this_user:
        counter += 1
    print counter

    context = {
        "u": u.first_name,
        "count": counter,
        "data_1": qoutes_by_this_user,
    }
    return render(request, 'quotes/details.html', context)


def addQuote(request):
    if "user_id" not in request.session:
        return redirect('/main')
    
    errors = Quote.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, errors, extra_tags=tag)
        return redirect('/quotes')
    else:
        qb = request.POST["quoted_by"]
        print qb
        q = request.POST['quote']
        print q
        u = User.objects.get( id = request.session['user_id'])
        print request.session['user_id']
        print u
        Quote.objects.create(quote = q,  quotedBy = qb, postedby = u)
        return redirect('/quotes')

# function that logs out a user
def logout(request):
    del request.session['user_id']
    return redirect('/main')