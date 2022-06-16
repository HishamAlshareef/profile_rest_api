from django.urls import path

from profiles_api import views

urlpatterns = [
    path('hello-view', views.HelloApiView.as_view()),
    # standard function that we call to convert our api view class tobe rendered by our urls
    # so basically Django rest framework will call this get function if a HTTP GET request is made to our URL
]