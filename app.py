from flask import Flask, render_template, redirect, url_for, request, session
from flask_session import Session
from flask import flash, get_flashed_messages, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, UserMixin, current_user
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os, json

# ALL THE MODULES INITIALISATION IS HERE
app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = '6bfd3f8b53ee37a07794664e'
# app.config["SESSION_PERMANENT"] = True
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


# ALL THE FORMS ARE HERE

class RegisterForm(FlaskForm):
    
    def validate_username(self, username_to_check):
        with app.app_context():
            user = User.query.filter_by(username=username_to_check.data).first()
            if user:
                raise ValidationError('Username already exists!')
            
    def validate_email_id(self, email_id_to_check):
        with app.app_context():
            email_id = User.query.filter_by(email_id=email_id_to_check.data).first()
            if email_id:
                raise ValidationError("Email already exists!")
               
    username = StringField(label='Username', validators=[Length(min=2, max=50), DataRequired()])
    email_id = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label="Log In")
    
class ImageUploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only Images Allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload')

class PostUploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only Images Allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    
    post_name = StringField(label="Post Name", validators=[DataRequired()])
    post_desc = StringField(label="Post Description", validators=[DataRequired()])
    
    submit = SubmitField('Upload')

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired(), Length(min=2)])
    submit = SubmitField()

class CommentForm(FlaskForm):
    comment = StringField(label='Add a Comment', validators=[DataRequired()])
    comment_post = StringField(label="Post Name")
    submit = SubmitField(label="Comment")
   
class SpecificPostForm(FlaskForm):
    post_name = StringField()
    submit = SubmitField("Visit Post")
    
# ALL THE MODELS ARE HERE

@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email_id = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    data = db.relationship('UserData', backref='owned_user', lazy=True)
    posts = db.relationship('Post', backref='owned_user', lazy=True)
     
    def __repr__(self):
        return f'User {self.username}'
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String())
    comment_post = db.Column(db.String())
    owner = db.Column(db.Integer(), db.ForeignKey('post.id'), nullable=False)
    
class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String()) 
    followers = db.Column(db.String())
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posts = db.Column(db.String())
    post_name = db.Column(db.String(), unique=True)
    post_desc = db.Column(db.String())
    comment = db.relationship('Comment', backref='commenter', lazy=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search = db.Column(db.String())

class LikeDislike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String())

class SpecificPostName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    specific_post_name = db.Column(db.String()) 

# ALL THE FUNCTIONS ARE HERE  
def add_user(username, email_id, password):
    user_to_add = User(username=username, email_id=email_id, password=password)
    with app.app_context():
        db.session.add(user_to_add)
        db.session.commit()
  
def save_image(picture_file):
    if picture_file != None:
        picture_name = picture_file.filename
        picture_path = os.path.join(app.root_path, 'static/uploads', picture_name)
        picture_file.save(picture_path)
        return picture_name
  
def add_profile(profile_image):
    if profile_image!=None:
        user = UserData(profile_image=profile_image, owner=current_user.username)
        db.session.add(user)
        db.session.commit()

def save_post(picture_file):
    if picture_file!=None:
        picture_name = picture_file.filename
        picture_path = os.path.join(app.root_path, 'static/uploads', picture_name)
        picture_file.save(picture_path)
        return picture_name

def add_post(post_image, post_name, post_desc):
    if post_image!=None:
        post = Post(posts=post_image, post_name=post_name, post_desc=post_desc, owner=current_user.username)
        db.session.add(post)
        db.session.commit()

def get_users_as_list():
    list = []
    i=1
    while (i<=len(User.query.all())):
        user = User.query.filter_by(id=i).first().username
        list.append(user)
        i += 1
    return list

#ALL THE ROUTES ARE HERE

@app.context_processor
def base():
    form = SearchForm()
    return dict(search_form=form)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    form = LoginForm()
    
    if form.validate_on_submit():
        with app.app_context():
            attempted_user = User.query.filter_by(username=form.username.data).first()
            username = str(attempted_user).lstrip('User ')
            attempted_pass = form.password.data
            real_pass = User.query.filter_by(username=form.username.data).first().password
            if attempted_user and attempted_pass == real_pass:
                login_user(attempted_user)
                return redirect(url_for(f'profile_page', data=attempted_user))
            else:
                flash("Username and Password doesn't match!", category='danger')
                
    return render_template('index.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    
    if form.validate_on_submit():
        add_user(form.username.data, form.email_id.data, form.password1.data)
        return redirect(url_for('home_page'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
        
    return render_template('register.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    form = ImageUploadForm()
    post_form = PostUploadForm()
    search_form = SearchForm()
    
    if form.validate_on_submit():
        image_file = save_image(form.photo.data)
        add_profile(image_file)
        
    if search_form.validate_on_submit():
        search_data = search_form.searched.data
        search_to_add = Search(search=search_data)
        db.session.add(search_to_add)
        db.session.commit()
        user_list = get_users_as_list()
        if search_data in user_list:
            return redirect(url_for('search_page', search_data=search_data))
        else:
            return f"<h1>Not Found Error 404</h1>"
        
    if post_form.validate_on_submit():
        post_form.photo.data.seek(0)
        post_file = save_image(post_form.photo.data)
        post_name = post_form.post_name.data
        post_desc = post_form.post_desc.data
        add_post(post_file, post_name, post_desc)
        
        
    str_user = str(current_user).lstrip('User').lstrip()
    user = UserData.query.filter_by(owner=str_user).all()
    if len(user)>=1:
        image_name = user[len(user)-1].profile_image
    else:
        image_name = ""
        
    profile_user = Post.query.filter_by(owner=current_user.username).all()
    post_name_list = ["default"]
    post_desc_list = ["default"]
    posts_list = ["default"]
    if len(profile_user)>=1:
        for postname in profile_user:
            post_name_list.append(postname.post_name)
            post_desc_list.append(postname.post_desc)
            posts_list.append(postname.posts)  
    else:
        pass
    
    length_of_post = len(post_name_list)
        
    return render_template('profile.html', form=form, post_form=post_form, image=image_name, search_form=search_form, post_name_list=post_name_list, post_desc_list=post_desc_list, posts_list=posts_list, length=length_of_post)


@app.route('/search')
def search_page():
    form = ImageUploadForm()
    post_form = PostUploadForm()
    
    if form.validate_on_submit():
        image_file = save_image(form.photo.data)
        add_profile(image_file)
    
    search_query = Search.query.filter_by(id=len(Search.query.all())).first().search
    
    user = UserData.query.filter_by(owner=search_query).all()
    if len(user)>=1:
        image_name = user[len(user)-1].profile_image
    else:
        image_name = ""
        
    
    profile_user = Post.query.filter_by(owner=search_query).all()
    post_name_list = ["default"]
    post_desc_list = ["default"]
    posts_list = ["default"]
    if len(profile_user)>=1:
        for postname in profile_user:
            post_name_list.append(postname.post_name)
            post_desc_list.append(postname.post_desc)
            posts_list.append(postname.posts)  
    else:
        pass
    
    length_of_post = len(post_name_list)
    

    return render_template('search.html', form=form, post_form=post_form, image=image_name, search_data=search_query, length=length_of_post, post_desc_list=post_desc_list, post_name_list=post_name_list, posts_list=posts_list)

@app.route('/feed', methods=['GET','POST'])
def feed_page():
    specific_form = SpecificPostForm()
    
    if specific_form.validate_on_submit():
        post_data = specific_form.post_name.data
        session["post_data"] = post_data
        specificpostname = SpecificPostName(specific_post_name=post_data)
        db.session.add(specificpostname)
        db.session.commit()
        return redirect(url_for(f'specific_post', post_data=post_data))
    
    posts = Post.query.all()
    posts.reverse()
    post_name_list = ["default"]
    post_desc_list = ["default"]
    posts_list = ["default"]
    post_owner = ["default"]
    if (len(posts)>1):
        for post in posts:
            post_name_list.append(post.post_name)
            post_desc_list.append(post.post_desc)
            posts_list.append(post.posts)
            post_owner.append(post.owner)
    else:
        pass
    
    length = len(post_name_list)
    
    return render_template('feed.html', post_owner=post_owner, post_desc_list=post_desc_list, post_name_list=post_name_list, posts_list=posts_list, length=length, specific_form=specific_form)

@app.route('/specificpost', methods=['GET', 'POST'])
def specific_post():
    form = CommentForm()
    data = session.get("post_data")
    
    if form.validate_on_submit():
        comment_text = form.comment.data
        comment_to_add = Comment(comment_text=comment_text, owner=current_user.username, comment_post=data)
        db.session.add(comment_to_add)
        db.session.commit()
    
    comment_to_show = Comment.query.filter_by(comment_post=data).all()
    comment_to_show.reverse()
    comment_text_list = ["default"]
    comment_owner_list = ["default"]
    if (len(comment_to_show)>1):
        for comments in comment_to_show:
            comment_text_list.append(comments.comment_text)
            comment_owner_list.append(comments.owner)
    else:
        pass  
      
    length = len(comment_text_list)
   
    username = Post.query.filter_by(post_name=data).first().owner
    post_image = Post.query.filter_by(post_name=data).first().posts
    post_desc = Post.query.filter_by(post_name=data).first().post_desc
    
    return render_template('specificpost.html', username=username, post_image=post_image, data=data, post_desc=post_desc, form=form, length=length, comment_text_list=comment_text_list, comment_owner_list=comment_owner_list)
