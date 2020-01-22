from flask import Flask,request, redirect, render_template, current_app
from flask_sqlalchemy import SQLAlchemy
import os
import secrets
from PIL import Image

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:fire@localhost:3306/postdb'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# convert of image 
def save_image(photo):
    # filename = os.path.dirname(os.path.abspath(__file__))
    rand_hex  = secrets.token_hex(10)
    i = Image.open(photo)
    _, file_extention = os.path.splitext(i)
    file_name = rand_hex + file_extention
    file_path = os.path.join(current_app.root_path, 'static/images', file_name)
    i.save(file_path)
    return file_name


# db post creation  table
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(100), default='image.jpg')
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return str(Post.id)


@app.route('/')
def index():
    return "Welcome to post"


# post root and insert 

@app.route('/post', methods=['POST','GET'])
def post_image():
    if(request.method == 'POST'):
        post_title = request.form['title']
        post_i = save_image(request.files.get('photo'))
        post_content = request.form['content']
        db.session.add(Post(title=post_title, image=post_i, content=post_content))
        db.session.commit()
        return redirect('/post')
    else:
        return render_template('index.html')


if(__name__ =='__main__'):
    app.run(debug=True)