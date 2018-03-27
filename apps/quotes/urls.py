from django.conf.urls import url
from . import views

urlpatterns = [
    # route to render login.html page
    url(r'^main$',  views.renderMain),

    # route to register a new user     
    url(r'^register$',  views.register),

    # route to login a user    
    url(r'^login$',  views.login),

    # route to render the trips table page     
    url(r'^quotes$',  views.renderQuotes),

    # route to add a quote to a users favorite
    url(r'^add/(?P<id>\d+)$',  views.add),
    
    # route to remove a quite from a users favorite
    url(r'^remove/(?P<id>\d+)$',  views.remove),
    
    # route to remove a quite from a users favorite
    url(r'^contributeQuote',  views.addQuote),
 
    # route to logout a user && del any sessions
    url(r'^logout$', views.logout),
    
    # route to logout a user && del any sessions
    url(r'^details/(?P<id>\d+)$', views.renderdetails),
    
]