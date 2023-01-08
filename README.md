Litracker - CS50_Final_Project
==============================
#### Name: Vasanthan S R
#### Username : srvasanthan33
#### Country : India
#### City : Chennai

-----
#### Video Demo: https://youtu.be/Cxg6rWa_-58

#### Description: **Litracker** is a light, Python/Flask web application which maintains the Book reading status of the user using Google Books API. This is for educational purpose on how the API works. It first stores the books which we are reading right now , then after every time we read the book we'll have to update the pages


##### Usage
------------
This is like regular web app, there is no complexity in using this app

1. Run `flask run` in the terminal
2. Once starting the site it can be seen on [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
3. Login page is loaded and we have to register
4. After Registering , index page is loaded . There the current books that the user is reading is shown
5. Users can add book by switching to `Add` section
6. Books are fetched using `Google Books API` based on the search results queried by the user
7. After Adding books, Pages read are updated in the main page below under drop selection
8. As the user start to update the page, it is seen on `Progress bar` below.
9. Users can also see the Leaderboard  and their Entries on the respective sections in `Nav-bar`

##### Tools used
--------------
.Flask framework
.Sqlite3 database engine
.Bootstrap CSS framework
.VS Code - Text Editor

##### Underlying details
--------
>1. Registering :

 For Registering I used registrants database which contains id, name username , pass_hash which converts user entered password to a hash file using password_hash_function

`CREATE TABLE registrants (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, username TEXT NOT NULL, pass_hash TEXT NOT NULL, points INTEGER NOT NULL DEFAULT 50);`

>2.  Logging in :

 After registering , user has to login for future entries. below command is used to check whether the enetred username is available in registrant or not.
`SELECT * FROM registrants WHERE username = ?", request.form.get("username")`

>3.  Adding Books:

After logging successfully user will have to add books to store it in their database. To fetch Books i used Google Books API. [https://www.googleapis.com/books/v1/volumes?q={searchParam}&](https://www.googleapis.com/books/v1/volumes?q={searchParam}&) This is what a google books api request link is. On typing the name of the query is parsed into the url and what we get is a JSON File from google API. I spent two days on how to handle this json request and surfed all over the internet and atlast i found a way. that is i used this code ,
`json_data = requests.get(main_api).json()` to fetch the json data and stored into dictionary by indexing each and every nested list of dictionary of dictionary of dictionary.....:(  , After obtaining the dictionary , i used jinja looping to display it in the add page below the search bar.

>4. Storing Books:

For Storing the books i used anothe route called `/process` which on POST request stores the book details into the `bookRecord` Table
`CREATE TABLE bookRecord (b_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, g_id TEXT NOT NULL, title TEXT NOT NULL, author TEXT NOT NULL, page INTEGER, image TEXT, username TEXT NOT NULL);`
and then redirection to the main page `/`

>5. Book Collections

After routing to `/` What it does is to display the added books of the user in the main  page which uses `card` for displaying. Not only dispalying it also contains a form for updating the pages we have read today which on clicking updates the `card` no of pages / total pages and a progress bar i have implemented this progress bar by altering the width of it based on percentages calculated by `jinja set` To store the Logs I implemented the table called `bookLog` for storing the time , no of pages and status of the book of the user currnetly reading


>6. Updating Points

To implemnt this I  computed the points by no of page sread by the user

>7. Leaderboard and Insight

For displayig the leaderboard is impl used SQL queries , Jinja Looping , CSS styling for tables to display them all
which is quite easy tahan the above two process





### Output :
![Screenshot (151)](https://user-images.githubusercontent.com/102546622/210108805-9f3e8662-3c92-4fd2-80eb-b0c9dddd02a6.png)

![Screenshot (150)](https://user-images.githubusercontent.com/102546622/210108818-6a9dcab2-59a6-4f2d-9807-55231ea84d5e.png)

![Screenshot (152)](https://user-images.githubusercontent.com/102546622/210108823-97d37c06-0bb4-41a9-83f7-bc1f954c0a93.png)

![Screenshot (158)](https://user-images.githubusercontent.com/102546622/210108976-76ac342a-0354-427c-be38-1dde14c31e74.png)

![Screenshot (155)](https://user-images.githubusercontent.com/102546622/210108985-6393ccda-d256-4126-89e0-91b273dd85a8.png)

![Screenshot (154)](https://user-images.githubusercontent.com/102546622/210108991-affe8fa1-cbe3-465d-8f37-2b2f1d2c6e2b.png)

![Screenshot (156)](https://user-images.githubusercontent.com/102546622/210109001-e33b8906-90ad-4b74-bb13-01ed306e8912.png)



>Credits
---------------
1. [Brad - Helped me in CSS,HTML](https://www.youtube.com/@LearnWebCode)
2. [Max Goodridge - for making me to understand JSON](https://www.youtube.com/@MaxGoodridgeTech)
3. And People of `STACK OVERFLOW` Who helped in many situations while developing this project

`Thank you` for all the staffs of **CS50**
============================
