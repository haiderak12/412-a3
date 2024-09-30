## restaurant/views.py
## description: write view functions to handle URL requests for the restaurant app

from django.shortcuts import render, redirect
import time
import random
from datetime import datetime, timedelta

# Create your views here.

SPECIALS = [
    "Special sauce",
    "Really special sauce",
    "Everything bowl",
    "Sprite cranberry",
    "Travis scott burger",
]

def main(request):
    '''Display the main page'''

    template_name = "restaurant/main.html"

    context = {
        "current_time": time.ctime(),
    }

    return render(request, template_name, context)

def order(request):
    '''Display the ordering page and daily special item'''

    template_name = "restaurant/order.html"

    context = {
        "current_time": time.ctime(),
        "special": random.choice(SPECIALS),
    }
    
    return render(request, template_name, context)

def confirmation(request):
    '''Process submission of order'''
    
    template_name = "restaurant/confirmation.html"

    # check that we have a POST request
    if request.POST:

        # Define menu items with their prices
        items_prices = {
            'chicken_bowl': 8,
            'steak_bowl': 10,
            'shrimp_bowl': 10,
            'chips': 3,
            'drink': 1,
        }

        specials_prices = {
            "Special sauce": 1,
            "Really special sauce": 2,
            "Everything bowl": 12,
            "Sprite cranberry": 2,
            "Travis scott burger": 6,
        }

        ordered_items = []
        total_price = 0

        # Check for each item if it was ordered
        for item, price in items_prices.items():
            if item in request.POST:
                ordered_items.append(f"{item.replace('_', ' ').title()} - ${price}")
                total_price += price

        # Handle the special item
        if 'special' in request.POST:
            special_name = request.POST['special']
            special_price = specials_prices.get(special_name, 5)  # Default price if not found
            ordered_items.append(f"{special_name} - ${special_price}")
            total_price += special_price

        # Get special instructions and customer info
        special_instructions = request.POST.get('special_instructions', '')
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')

        ready_time = datetime.now() + timedelta(minutes=random.randint(30, 60))

        context = {
            "current_time": time.ctime(),
            "ordered_items": ordered_items,
            "total_price": total_price,
            "special_instructions": special_instructions,
            "name": name,
            "phone": phone,
            "email": email,
            "ready_time": ready_time,
        }

        return render(request, template_name, context)
    
    return redirect("order")