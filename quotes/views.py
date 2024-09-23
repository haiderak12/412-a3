## quotes/views.py
## description: write view functions to handle URL requests fro the quotes app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random
import time

QUOTES = [
    "I love sleep, it's my favorite.",
    "I'm nice at ping pong.",
    "I am not a fan of books.",
    "I feel like I'm too busy writing history to read it.",
    "I have decided in 2020 to run for president.",
    "I don't use blue. I don't like it. It bugs me out. I hate it.",
    "I don't think people are going to talk in the future. They're going to communicate through eye contact, \
        body language, emojis, signs.",
    "I don't even listen to rap. My apartment is too nice to listen to rap in.",
    "Nobody can tell me where I can and can't go.",
    "If I was a fan of music, I would think that I was the number one artist in the world."
]

IMAGES = [
    "https://cdn.britannica.com/00/236500-050-06E93F4F/Kanye-West-2018.jpg",
    "https://compote.slate.com/images/1e778761-444d-45da-9192-abc1e930d571.jpg",
    "https://andscape.com/wp-content/uploads/2018/05/gettyimages-509641192_master.jpg",
    "https://compote.slate.com/images/2fe5965c-9b5a-44ab-ae7f-1f8feb0afdd2.jpeg?crop=1560%2C1040%2Cx0%2Cy0",
    "https://thefader-res.cloudinary.com/private_images/w_760,c_limit,f_auto,q_auto:best/GettyImages-1366399279_aof5rr_k2djrl/kanye-west.jpg",
    "https://i.imgur.com/J6y1iJs.png"

]

# Create your views here.
def quote(request):
    '''
    Function to handle the URL request for /quote (main page).
    Delegate rendering to the template hw/quote.html.
    '''
    # Render the response
    template_name = 'quotes/quote.html'

    quote = random.choice(QUOTES)
    image = random.choice(IMAGES)

    context = {
        'current_time' : time.ctime(),
        'quote': quote,
        'image': image
    }

    # Delegate rendering work to the template
    return render(request, template_name, context)

def show_all(request):
    '''
    Function to handle the URL request for /show_all (main page).
    Delegate rendering to the template hw/show_all.html.
    '''
    # Render the response
    template_name = 'quotes/show_all.html'

    context = {
        "current_time" : time.ctime(),
        'quotes': QUOTES,
        'images': IMAGES
    }

    # Delegate rendering work to the template
    return render(request, template_name, context)

def about(request):
    '''
    Function to handle the URL request for /about (main page).
    Delegate rendering to the template hw/about.html.
    '''
    # Render the response
    template_name = 'quotes/about.html'

    context = {
        "current_time" : time.ctime()
    }

    # Delegate rendering work to the template
    return render(request, template_name, context)