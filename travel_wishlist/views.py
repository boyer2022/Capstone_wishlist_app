# Original code at https://github.com/claraj/django_travel_wishlist
# Finished code at https://github.com/claraj/wishlist_with_uploads

from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required
# Create your views here.
def place_list(request):
    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)   # Creating a form from data in the request
        place = form.save(commit=False)                 # .save() is making a model object
        place.user = request.user
        if form.is_valid():                 # if valid - validation against DB constraints
            place.save()                    # saves place to DB
            return redirect('place_list')   # Reloads home page

    # Making call to DB
        # Fetches ALL of the places(objects) from DB
    # places = Place.objects.all()
            # OR
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()         # Used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

@login_required
def place_was_visited(request, place_pk):           # place_pk is a variable from url.py
    # Only responds to POST requests
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)
# 404 error- Use Dev tools as Network-fetch, paste in Console, change pk to incorrect number, 'Enter'
        place = get_object_or_404(Place, pk=place_pk)   
        if place.user == request.user:
            place.visited = True
            place.save()                        # Saves to DB, must be saved to  be in DB
        else:
            return HttpResponseForbidden()
    return redirect('place_list')

@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })

@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    # Does this place belong to the user?
    if place.user != request.user:
        return HttpResponseForbidden()
    #Is this a GET request(show data/form) or a POST request (update Place object)?

    # If POST request, validate form data and update
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip Information Updated!')
        else:
            messages.error(request, form.errors)        # Temp message, refine later
        
        return redirect('place_details', place_pk=place_pk) 

    else:
        # If GET request, show Place info and optional form.
        # If place is visited, show form, if place is not visited, no form.
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form })
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()


@login_required
# Requested from about.html
def about(request):
    author = 'Matt'
    about = "A website to create a list of places to visit"
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})
