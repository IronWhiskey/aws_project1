from django.conf.urls import url
from . import views

urlpatterns = [
    # route to render login.html page
    url(r'^main$',  views.renderLogin),

    # route to register a new user     
    url(r'^register$',  views.register),

    # route to login a user    
    url(r'^login$',  views.login),     
    # route to render the trips table page     
    url(r'^travels$',  views.renderTrips),

    # route to add a user to a specific trip
    url(r'^join/(?P<trip_id>\d+)$',  views.join),

    # route to render the addPlan.html page
    url(r'^travels/add$',  views.renderAddPlan),

    # route to render the addPlan.html page
    url(r'^addplan$',  views.addPlan),

    # route to get details on a trip
    url(r'^details/(?P<trip_id>\d+)$',  views.details),

    # route to render the details page
    url(r'^travels/destination/(?P<trip_id>\d+)$',  views.renderDetails),

    # route to logout a user && del any sessions
    url(r'^logout$', views.logout),

    # route to render the logout/goodby page before redirecting to index.html
    url(r'^goodbye$', views.renderGoodbye), 
]