import os
import requests
import urllib.parse
import json

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code
    

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# which send book queries in the form of list >> dictionary
def book_finder(searchParam):
    main_api = f"https://www.googleapis.com/books/v1/volumes?q={searchParam}&maxResults=5"

    #after we got the url , we are going to parse into json() w

    json_data = requests.get(main_api).json()
 

    # storing json data into the python_dictionary
    try:
        BOOKLIST = []
        for i in range(3): # To send maximum 3 data
            BOOK = {}
            data = json_data["items"][i]
            try:    
                BOOK["id"] = data["id"]
                BOOK["title"] = data["volumeInfo"]["title"]
                BOOK["author"] = data["volumeInfo"]["authors"][0]
                BOOK["description"] = data["volumeInfo"]["description"]
                BOOK["pages"] = int(data["volumeInfo"]["pageCount"])
                BOOK["image"] = data["volumeInfo"]["imageLinks"]["smallThumbnail"]

            except:
                BOOK["pages"] = None
                BOOK["image"] = data["volumeInfo"]["imageLinks"]["smallThumbnail"]

            BOOKLIST.append(BOOK)
        return BOOKLIST

    except (KeyError, TypeError, ValueError):
        return None

