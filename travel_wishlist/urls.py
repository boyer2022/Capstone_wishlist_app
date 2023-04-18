from django.urls import path
from . import views

urlpatterns = [
    # list of urls app will recognize
    # request to the path empty string, home page
        # 'Any request made to the home page, should be handled by a function called place_list in the views module
    path('', views.place_list, name='place_list'),
    # Places visited
    path('visited', views.places_visited, name='places_visited'),

    # Path for new places to visit/have visited
    path('place/<int:place_pk>/was_visited', views.place_was_visited, name='place_was_visited'),

    # Creating an 'about' page for the HTML
    path('about', views.about, name='about')
    

]