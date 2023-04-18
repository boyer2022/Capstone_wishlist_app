from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.
def place_list(request):
    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)   # Creating a form from data in the request
        place = form.save()                 # .save() is making a model object
        if form.is_valid():                 # if valid - validation against DB constraints
            place.save()                    # saves place to DB
            return redirect('place_list')   # Reloads home page

    # Making call to DB
        # Fetches ALL of the places(objects) from DB
    # places = Place.objects.all()
            # OR
    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()         # Used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

def place_was_visited(request, place_pk):           # place_pk is a variable from url.py
    # Only responds to POST requests
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)       # 404 error- Use Dev tools as Network-fetch, paste in Console, change pk to incorrect number, 'Enter'

        place.visited = True
        place.save()                                # Saves to DB, must be saved to  be in DB
    return redirect('place_list')

def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })



# Requested from about.html
def about(request):
    author = 'Matt'
    about = "A website to create a list of places to visit"
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})
