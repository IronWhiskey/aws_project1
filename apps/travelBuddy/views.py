# Dev: Michael G.
# Date: 3/21/2018 
# Build with: python, django, html, css
# Description:  trip sharing application that stores and displays users upcoming trips
# and allows others to view and join their trips

#------------------------------------- IMPORTS --------------------------------------
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from .models import User, Trip
import bcrypt
from django.contrib import messages
#------------------------------------------------------------------------------------


# function that renders the login page
def renderLogin(request):
    if "user_id" not in request.session:
        request.session['user_id'] = False
    return render(request, 'travelBuddy/login.html')


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
        u_name = request.POST["username"]
        p = request.POST["password"]
        hp = bcrypt.hashpw( p.encode(), bcrypt.gensalt() )
        User.objects.create(first_name = f, last_name = l, username = u_name, password_hash = hp)
        u = User.objects.filter(username = u_name, password_hash = hp)[0]
        id = u.id   # get the user id of the user just registered
        request.session['user_id'] = id
    return redirect("/travels")


# function that renders the trips.html page
def renderTrips(request):
    #if the user_id is not in the session cookies were lost, redirect to the main login page
    if "user_id" not in request.session:
        return redirect('/main')

    u = User.objects.get(id = request.session['user_id'])

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
        "userName": u.first_name,
        "data_1": u.trips.all(),
        "data_2": Trip.objects.exclude(planner=u.id).exclude(attendee=u.id)
    }
    return render(request, 'travelBuddy/trips.html', context)


# function that gets user email and password from a POST on login page and checks for valid creds
def login(request):
    #if the user_id is not in the session cookies were lost, redirect to the main login page
    if "user_id" not in request.session:
        return redirect('/main')
    un = request.POST["username"]
    p = request.POST['password']
    hp = bcrypt.hashpw( p.encode(), bcrypt.gensalt() )
    # check if username/email and password exist in system
    temp_users = User.objects.filter(username = un)
    if len(temp_users) > 0:
        for n in temp_users:
            if (bcrypt.checkpw(p.encode(), n.password_hash.encode())):
                request.session['user_id'] = n.id
                return redirect('/travels') 
            else:
                # print 'inside else'
                messages.add_message(request, messages.INFO, 'Incorrect email and or password')
                return redirect('/main')
    return redirect('/main')


# function that joins a current user to an existing trip
def join(request, trip_id):
    #if the user_id is not in the session cookies were lost, redirect to the main login page
    if "user_id" not in request.session:
        return redirect('/main')
    u_id = request.session['user_id']
    u = User.objects.get(id=u_id)
    t = Trip.objects.get(id=trip_id)
    u.trips.add(t)
    return redirect('/travels')


# fucnction that renders the addPlan html
def renderAddPlan(request):
    #if the user_id is not in the session cookies were lost, redirect to the main login page    
    if "user_id" not in request.session:
        return redirect('/main')
    return render(request, 'travelBuddy/addPlan.html')


# function to add a new trip for a user
def addPlan(request):
    #if the user_id is not in the session cookies were lost, redirect to the main login page
    if "user_id" not in request.session:
        return redirect('/main')
    user_id = request.session['user_id']
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, errors, extra_tags=tag)
        return redirect('travels/add')
    else:
        
        destin = request.POST["destination"]
        descrip = request.POST["description"]
        start = request.POST["travel_start"]
        end = request.POST["travel_end"]
        u = User.objects.get(id=user_id)
        t = Trip.objects.create(planner = u, destination = destin, description = descrip, travel_start = start, travel_end = end)
        u.trips.add(t)
        return redirect("/travels")


def details(request, trip_id):
    #if the user_id is not in the session cookies were lost, redirect to the main login page
    if "user_id" not in request.session:
        return redirect('/main')
    return redirect('/travels/destination/{}'.format(trip_id))


def renderDetails(request, trip_id):
    #if the user_id is not in the session cookies were lost, redirect to the main login page    
    if "user_id" not in request.session:
        return redirect('/main')
    this_trip = Trip.objects.get(id=trip_id)
    person = this_trip.planner
    personName = person.first_name + ' ' + person.last_name
    attending = this_trip.attendee.exclude(id = person.id)
    context = {
        "planner": personName,
        "trip": this_trip,
        "attending": attending
    }
    return render(request, "travelBuddy/details.html", context)


# function to logout a user and redirect to login/register page
def logout(request):
    del request.session['user_id']
    return redirect('/main')


# function used to render the goodbye exit page
def renderGoodbye(request):
    return render(request, 'travelBuddy/goodbye.html')
    