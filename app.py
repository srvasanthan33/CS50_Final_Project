# importing Packages from flask , werk for password hahsing,
import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

from helpers import apology, login_required, book_finder,book_id
from datetime import datetime


# getting these config values from cs50 problem_set finance
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
#app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Importing my database{project.db} with cs50 library 
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/",methods =["GET","POST"])
@login_required
def index():
    """ shows The three books read by user"""
    u_id = session["user_id"]
    rows = db.execute("SELECT * from registrants where id = ?",u_id)

    name = rows[0]["name"]
    username = rows[0]["username"]
    points = rows[0]["points"]
    BOOKS = db.execute("SELECT * FROM bookRecord WHERE username = ? ;",username)
    
    if request.method == "GET":
    
        count = 0
        image = []
        for BOOK in BOOKS:
            image.append(BOOK["image"])
            count += 1

        # to get current page
        query = db.execute("select title,MAX(currentPage) as currentPage FROM bookLog WHERE username = ? GROUP BY title ORDER BY b_id;",username)
        
        return render_template("index.html",BOOKS = BOOKS,name=name,points=points,image=image,count=count,query = query)

    elif request.method == "POST":
        Book_title = request.form.get("Book_name")
        pages = request.form.get("pages_read")
        
        if not pages or not Book_title:
            return apology("error occured")
        pages = int(pages)

        BOOK = db.execute("SELECT * FROM bookRecord WHERE username = ? AND title = ? ;",username, Book_title)

        Time = datetime.now()
        # point Calculator
        point = rows[0]["points"] + pages*1

        if pages > BOOK[0]["page"]:
            return apology("Pages Exceeded")

        if pages < BOOK[0]["page"]:
            db.execute("INSERT INTO bookLog (b_id, title, currentPage, username, time) VALUES(?, ?, ?, ?, ?)",BOOK[0]["g_id"],BOOK[0]["title"],pages,username,Time)
            
            db.execute("UPDATE registrants SET points = ? WHERE username = ?",point,username)
        else:
            db.execute("INSERT INTO bookLog (b_id, title, currentPage, status, username, time) VALUES(?, ?, ?, ?, ?, ?)",BOOK[0]["g_id"],BOOK[0]["title"],BOOK[0]["page"],'Completed',username,Time)

            db.execute("UPDATE registrants SET points = ? WHERE username = ?",point,username)
        
        
        
        return redirect("/")

    



    



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM registrants WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["pass_hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
        
    elif request.method == 'POST':
        Name = request.form.get("Name")
        Username = request.form.get("Username")
        Password1 = request.form.get("Password")

        userbase = db.execute("SELECT * FROM registrants WHERE username = ?",Username)
        if len(userbase) == 1:
            return apology("Username already taken")

        #hashing the password
        Password_hash = generate_password_hash(Password1) 

        # if all the inputs are correct then store the details into the database
        db.execute("INSERT INTO registrants (name, username, pass_hash) VALUES(?, ?, ?)",Name, Username, Password_hash)

        # To find the used id from database which we inserted in the above , to store it in the session
        rows = db.execute("SELECT id FROM registrants WHERE username = ?", Username)
        session["user_id"] = rows[0]["id"]

        # redirecting to main(index) page
        return redirect("/")

    return apology("Error",404)



@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Will update the reading """
    image = []
    if request.method == "GET":
        u_id = session["user_id"]
        rows = db.execute("SELECT * from registrants where id = ?",u_id)

        name = rows[0]["name"]
        username = rows[0]["username"]
        points = rows[0]["points"]



        return render_template("add.html",points=points,image = image)
    
    # POST Requests
    # from search input of book 
    
    
    try:
        search = request.form.get("BookSearch")
        BOOKLIST = book_finder(search)

        for BOOK in BOOKLIST:
            image.append(BOOK["image"])
    except :
        return apology("Book Not Found")
    
    
    return render_template("add.html",BOOKLIST=BOOKLIST,image=image)

@app.route("/process", methods=["GET", "POST"])
@login_required
def process():
    if request.method == "POST":
        c = request.form.get('btn')
        BOOK = book_id(c)

        #To get username
        userId = session.get("user_id")
        USERPortfolio = db.execute("SELECT * FROM registrants WHERE id = ?", userId)
        USERNAME = USERPortfolio[0]["username"]

        Time = datetime.now()
        db.execute(
            "INSERT INTO bookRecord (g_id, title, author, page, image, username) VALUES(?, ?, ?, ?, ?, ?)", BOOK["id"], BOOK["title"], BOOK["author"], BOOK["pages"], BOOK["image"],USERNAME)

        db.execute(
            "INSERT INTO bookLog (b_id, title, currentPage, username, time) VALUES(?, ?, ?, ?, ?)",BOOK["id"], BOOK["title"], 0, USERNAME, Time)

        return redirect("/")
    elif request.method == "GET":
        return apology("sdfsd")


    #return apology("ADD")

@app.route("/leaderboard", methods=["GET", "POST"])
@login_required
def leaderboard():
    """Based on reading consistency , reaability user will get rankings"""

    if request.method == 'GET':
        # getting username from the session
        u_id = session["user_id"]
        rows = db.execute("SELECT * from registrants where id = ?",u_id)

        name = rows[0]["name"]
        username = rows[0]["username"]  
        points = rows[0]["points"]  

        ROWS = db.execute("SELECT name, username, points FROM  registrants ORDER BY points desc")
        LOGS = []
        for i in range(len(ROWS)):
            D = {}
            D["id"] = i + 1
            D["name"] = ROWS[i]["name"]
            D["username"] = ROWS[i]["username"]
            D["points"] = ROWS[i]["points"]
            LOGS.append(D)

        return render_template("leaderboard.html",LOGS = LOGS,points = points)
    return apology("leaderboard")


@app.route("/logs", methods=["GET", "POST"])
@login_required
def logs():
    """Shows what updates the user had done"""

    if request.method == 'GET':
        # getting username from the session
        u_id = session["user_id"]
        rows = db.execute("SELECT * from registrants where id = ?",u_id)

        name = rows[0]["name"]
        username = rows[0]["username"]  
        points = rows[0]["points"]  

        ROWS = db.execute("SELECT * FROM bookLog WHERE username = ? ORDER BY id;",username)   
        LOGS = []
        
        for R in ROWS:
            D = {}
            D["id"] = R["id"]
            D["title"] = R["title"]
            D["page"] = R["currentPage"]
            D["status"] = R["status"]
            D["time"] = R["time"]
            LOGS.append(D)
        

        return render_template("log.html",points=points,LOGS=LOGS)

        
    return apology("Logs")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
    










