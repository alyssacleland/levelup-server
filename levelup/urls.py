"""
URL configuration for levelup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from levelupapi.views import GameTypeView, EventView, GameView
from django.urls import path
from levelupapi.views import register_user, check_user


# The trailing_slash=False tells the router to accept /gametypes instead of /gametypes/. It’s a very annoying error to come across, when your server is not responding and the code looks right, the only issue is your fetch url is missing a / at the end.
router = routers.DefaultRouter(trailing_slash=False)
# The next line is what sets up the /gametypes resource (see more with visual: https://github.com/nashville-software-school/server-side-python-curriculum/blob/evening-cohorts/book-3-levelup/chapters/LU_LIST_RETRIEVE.md). more below @ bottom
router.register(r'gametypes', GameTypeView, 'gametype')
router.register(r'events', EventView, 'event')
# This line is added to register the GameView
router.register(r'games', GameView, 'game')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  # add router variable to urlpatterns
    path('register', register_user),
    path('checkuser', check_user),
]

# Each path() in urlpatterns is mapping a URL pattern to a view — which is just the code that runs when someone visits that URL.


# The first parameter, r'gametypes, is setting up the url.
# The second GameTypeView is telling the server which view to use when it sees that url.
# The third, gametype, is called the base name. You’ll only see the base name if you get an error in the server. It acts as a nickname for the resource and is usually the singular version of the url.
