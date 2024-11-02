from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from dotenv import load_dotenv
import os

BASE_URL=os.getenv('BASE_URL')
API_KEY=os.getenv('API_KEY')
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
   __tablename__ = 'User'
   username = db.Column(db.String(50),primary_key=True)
   password = db.Column(db.String(50),nullable=False)
   fullname = db.Column(db.String(50),nullable=False)

   def __repr__(self) -> str:
      return f'{self.fullname} --------- {self.username} ----------- {self.password}'

class BookMarks(db.Model):
   __tablename__ = 'bookmarks'
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(50),nullable=False)
   title  = db.Column(db.String,nullable=False)
   url  = db.Column(db.String,nullable=False)
   urlToImage = db.Column(db.String,nullable=False)
   description = db.Column(db.String,nullable=False)
   publishedAt = db.Column(db.String, nullable=False)

   def __repr__(self) -> str:
      return f'{self.username} ----------- {self.id} ----------- {self.publishedAt}'


@app.route('/logout/', methods=['GET','POST'])
def logout():
   session.pop('username', None)
   return redirect(url_for('login',message="You have been logged out.!!"))

@app.route('/login/', methods=['GET','POST'])
def login():
   message = request.args.get('message')
   if request.method == 'POST':
      form = request.form
      username= form.get('username')
      password= form.get('password')
      print(username)
      print(password)
      if username:
         user = User.query.filter_by(username = username).first()
         print(user)
         if user and user.password == password:
            session['username'] = user.username
            return redirect(url_for('home',message=f"Welcome {user.fullname}"))
         else:
            return render_template('login.html',message="Incorrect credentials!!") 
   
   return render_template('login.html',message=message)

@app.route('/signup/', methods=['GET','POST'])
def signup():
   if request.method == 'POST':
      form = request.form
      username= form.get('username')
      fullname= form.get('fullname')
      password= form.get('password')
      confirm_password= form.get('confirm_password')
      print(username)
      print(fullname)
      print(password)
      print(confirm_password)
      if username:
         user = User.query.filter_by(username = username).first()
         print(user)
         if user:
            return redirect(url_for('login',message="User already exists.!!"))
         else:
            if password == confirm_password:
               new_user = User(username=username,fullname=fullname,password=password)
               db.session.add(new_user)
               db.session.commit()
               session['username'] = username
               return redirect(url_for('home',message=f"Welcome {fullname}!!"))
            else:
               return render_template('signup.html',message="Passwords don't match.!!")
            
   return render_template('signup.html')

@app.route('/')
def home():
   message = request.args.get('message')
   if "username" in session:
      URL=f'{BASE_URL}/top-headlines?country=us&apiKey={API_KEY}'
      data = requests.get(URL)
      data = data.json()
      articles = data.get('articles', [])
      with open('articles.json','w') as file:
         # json.dump(articles,file,indent=4)
         print("written!!")
      file.close()
      if len(articles) > 20:
         articles = articles[:20] 
      return render_template('index.html',news_articles=articles,title="Top Headlines",message=message)
   return redirect('login/')
  
@app.route('/search/', methods=['POST'])
def search():
   query = request.form.get('query')
   if "username" in session and  query :
      URL=f'{BASE_URL}/everything?q={query}&apiKey={API_KEY}'
      data = requests.get(URL)
      data = data.json()
      print(URL)
      articles = data.get('articles', [])
      with open('articles.json','w') as file:
         # json.dump(articles,file,indent=4)
         print("written!!")
      file.close()
      if len(articles) > 20:
         articles = articles[:20]
      
      return render_template('index.html',news_articles=articles,query=query,title="Top Headlines")
   
   return redirect('login')

@app.route('/category/', methods=['GET'])
def category():
   query = request.args.get('category')
   if "username" in session and query:
         URL=f'{BASE_URL}/top-headlines?category={query}&apiKey={API_KEY}'
         data = requests.get(URL)
         data = data.json()
         print(URL)
         articles = data.get('articles', [])
         with open('articles.json','w') as file:
            # json.dump(articles,file,indent=4)
            print("written!!")
         file.close()
         if len(articles) > 20:
            articles = articles[:20]
         return render_template('index.html',news_articles=articles,query=query,title=query)
   
   return redirect(url_for('login'))
      

@app.route('/add_bookmark/',methods=["POST","GET"])
def add_bookmark():
   message = request.args.get('message')
   if request.method=="POST" and  "username" in session:
      username = request.form.get("username")
      title = request.form.get("title")
      url = request.form.get("url")
      urlToImage = request.form.get("urlToImage")
      description = request.form.get("description")
      publishedAt = request.form.get("publishedAt")
      print({username,title,url,urlToImage,publishedAt,description})

      new_bookmark = BookMarks(username=username,title=title,url=url,urlToImage=urlToImage,publishedAt=publishedAt,description=description)

      db.session.add(new_bookmark)
      db.session.commit()
      return redirect(url_for('home',message=message))
   
   return redirect('login/')

@app.route('/bookmarks/',methods=['GET','POST'])
def bookmarks():
   message = request.args.get('message')
   if "username" in session:
      if request.method == "GET":
         bookmarks = BookMarks.query.filter_by(username=session['username']).all()
         print(bookmarks)
         return render_template('bookmark.html',bookmarks=bookmarks,message=message)
      if request.method == "POST":
         id = request.form.get('id')
         print(id)
         bookmark = BookMarks.query.filter_by(id=int(id)).first()
         print(bookmark)
         if bookmark:
            db.session.delete(bookmark)
            db.session.commit() 
         return redirect(url_for('bookmarks',message='Bookmark removed!!'))
      
   return redirect(url_for('login'))

if __name__ == '__main__':
   with app.app_context():
      db.create_all()
   app.run(debug=True) 