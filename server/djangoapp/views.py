from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .models import CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)

# View to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# View to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# View to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['password']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('/djangoapp')
        else:
            # If not, return to login page again
            return redirect('/djangoapp')
    else:
        return render(request, 'djangoapp/index.html', context)        

# View to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user '{}'".format(request.user.username))
    # Logout the user in the request
    logout(request)
    # Redirect user back to the index
    return redirect('/djangoapp')

# View to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it a POST request
    elif request.method == 'POST':
        # Get the user information from request.POST
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is a new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            # Login the user and redirect to index page
            login(request, user)
            return redirect('/djangoapp')
        else:
            return render(request, 'djangoapp/registration.html', context)

# View to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        # Get_dealership function API url
        url = "https://9a6517f2.us-south.apigw.appdomain.cloud/api/dealership/api/dealership"
        # Return the dealership data
        dealerships = get_dealers_from_cf(url)
        context = dealerships
        return render(request, 'djangoapp/index.html', {"list" : context})

# View to render a page with the dealer details
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        # Get_review function API url
        url = "https://9a6517f2.us-south.apigw.appdomain.cloud/api/review/api/review"
        # Return the reviews data
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        # Print the review
        context["reviews"] = reviews
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a add_review view to submit a review
def add_review(request, dealer_id):
    context = {}
    user = request.user
    if request.user.is_authenticated:
        
        # If GET request sen user to add review form page
        if request.method == "GET":
            context["cars"] = list(CarModel.car_manager.all().filter(dealer_id=dealer_id))
            context["dealer_id"] = dealer_id
            # Return dealers cars to use in select form
            return render(request, 'djangoapp/add_review.html', context) 
        
        # If POST request add new review to database
        elif request.method == "POST":
            car_id = request.POST["car"]
            car = CarModel.car_manager.get(pk=car_id)
            username = request.user.username
            
            # Populate the review dict
            review = dict()
            review["id"] = dealer_id
            review["name"] = username  
            review["dealership"] = dealer_id
            review["review"] = request.POST["content"]
            review["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    review["purchase"] = True
            review["purchase_date"] = request.POST["purchasedate"]
            review["car_make"] = car.carmake.name
            review["car_model"] = car.name
            review["car_year"] = int(car.year)
                        
            json_review = dict()
            json_review["review"] = review
            
            # Add the review trough the post_request function
            url = "https://9a6517f2.us-south.apigw.appdomain.cloud/api/review/api/review"
            json_data = post_request(url, json_review)
            
            # Return the user to the dealer_details page
            return redirect('djangoapp:dealer_details', **{"dealer_id":dealer_id}) 

# Pass the dealer_id to the dealer_details page
def dealer_details(request, dealer_id):
    context = {"id":dealer_id}
    return render(request, 'dealer_details.html', context)