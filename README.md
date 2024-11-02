# README.md (**_Flask NewsApp_**)

## This is a fullstack flask news app with support of databse and authentication. The news is coming from the [_Newsapi.org API_](https://newsapi.org/)

- User can login and signup.
- Also they can bookmark their favorite news articles and these infomation are stored in database in two tables **Users** and **Bookmarks**
- They can see and remove their bookmarked articles in the **Bookmarks** section.

### Setup  

#### 1. Unzip the tar file

#### 2. Then go to directory where unzipped project is

#### 3. First install required modeules

` pip install -r requirements.txt `

#### 4. Go to directory having **app.py**

#### 5. Open terminal and type

` python app.py `

#### 6. Open browser and go to link

` http://localhost:5000 `

### 7. Features

1. First you have to login. ``(Dummy Username :  admin and Password : 123)``
2. You can see main news on home page.
3. You can see news on specific genere using dropdown _category_.
4. You can also search for specific topic using search bar in navbar.
5. You can bookmark any article and the articles then be bookmarked.
6. You can see the bookmarked articles in **Bookmark** section.

## Urls 
| Route                           | Description                               |
|---------------------------------|-------------------------------------------|
| `http://localhost:5000/login`   | Login Page                                |
| `http://localhost:5000/signup`  | Signup Page                               |
| `http://localhost:5000/`        | Home Page (If logged in)                  |
| `http://localhost:5000/search`  | Results for searched query (POST request) |
| `http://localhost:5000/category/?category=_{category}_` | News for specific category |
| `http://localhost:5000/bookmarks` | Bookmarks Page (If logged in)             |

