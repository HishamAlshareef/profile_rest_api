from django.urls import path, include

from rest_framework.routers import DefaultRouter

from profiles_api import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
# to register specific view sets with our router
# because the router will create all the four URLs for us, we don't need to specify a forward slash here when we
# define our view set URL names
# The second argument is the viewset that we wish to register to this URL
# The third argument going to be used for retrieving the URLs in our router
# if we ever need to do that using the URL retrieving function provided by Django
router.register('profile', views.UserProfileViewSet)  # no need to specify a base name argument and this is because
# we have in our view set a queryset object
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    # standard function that we call to convert our api view class tobe rendered by our urls
    # so basically Django rest framework will call this get function if a HTTP GET request is made to our URL
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls))  # as you register new routes with our router it generates a list of URLs that are
    # associated for our viewset it figures out the URLs that are required

    # The router generates multiple URLs for the resources which are registered to it. For example router.register(
    # 'feed', views.UserProfileFeedViewSet) will register multiple URLs like: /api/feed, /api/feel/:id. After
    # everything is registered to a router, you can get all urls at router.urls. The include() function is used to
    # include multiple URLs. So essentially all that line does it include URLs for everything that's registered to a
    # router.


]
