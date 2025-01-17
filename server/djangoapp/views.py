from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_request, get_dealer_reviews_from_cf, post_request

# Get an instance of a logger
logger = logging.getLogger(__name__)

current_user = ''

# Create your views here.

# Create an `about` view to render a static about page
def get_about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def get_contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    global current_user
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        current_user = username
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back 
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/072aa07a-e470-4574-a987-b30c76a2469d/default/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)

def get_dealer_details(request, dealer_id):
    context = {}
    context['dealer_id'] = dealer_id
    print(dealer_id)
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/072aa07a-e470-4574-a987-b30c76a2469d/default/review"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context['reviews'] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealer_Id):
    global current_user
    context = {}
    context['dealer_Id'] = dealer_Id
    if request.method == "GET":
        context['cars'] = CarModel.objects.all()
        return render(request, 'djangoapp/add_review.html', context)

    elif request.method == "POST":
        review = request.POST["content"]
        if 'purchasecheck' in request.POST:
            purchase = True
            purchasedate = request.POST["purchasedate"]
        else: 
            purchase = False
            purchasedate = None

        car = CarModel.objects.get(id=request.POST['car'])

        print(request.POST['car'])
        car_make = car.car_type
        car_model = car.name
        car_year = car.year.isoformat()

        url = "https://us-south.functions.appdomain.cloud/api/v1/web/072aa07a-e470-4574-a987-b30c76a2469d/default/post-review"
        review = {
            "time": datetime.utcnow().isoformat(),
            "dealership": dealer_Id,
            "review": review,
            "purchase": purchase,
            "name": current_user,
            "car_make": car_make,
            "car_model": car_model,
            "purchase_date": purchasedate,
            "car_year": car_year,
            "id": dealer_Id
                 }
        json_payload = {}
        json_payload['review'] = review
        post_request(url, json_payload, dealerId=dealer_Id)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_Id)


