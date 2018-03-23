from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$',  views.renderIndex),             # route to render index.html page
    url(r'^register$',  views.register),       # route to register user data
    url(r'^login$', views.login),              # route to login user
    url(r'^success/(?P<id>\d+)$', views.renderSuccess),    # route to render success.html page
    url(r'^logout$', views.logout),         # route to logout a user && del any sessions
    url(r'^goodbye$', views.renderGoodbye), # route to render the logout/goodby page before redirecting to index.html
]