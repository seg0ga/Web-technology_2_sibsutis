from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
import os
from werkzeug.utils import secure_filename
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videohost.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'qwerty666777'
login_manager = LoginManager(app)
login_manager.login_view = 'login'


app.config['UPLOAD_FOLDER'] = 'static/uploads/videos'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'mov', 'avi', 'mkv', 'webm'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship('User', backref='comments')
    post = db.relationship('Post', backref='comments')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    video_filename = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='posts')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        except:
            return render_template('register.html')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/posts')

        return redirect("/login")

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/posts')


@app.route("/posts")
@app.route("/")
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)


@app.route("/create", methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        if 'video' not in request.files:
            return "Нужно выбрать видеофайл"

        video_file = request.files['video']

        if video_file.filename == '':
            return "Файл не выбран"

        if not allowed_file(video_file.filename):
            return "Неподдерживаемый формат видео"

        filename = secure_filename(f"{current_user.id}_{video_file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video_file.save(filepath)

        post = Post(
            title=request.form['title'],
            text=request.form['text'],
            video_filename=filename,
            author=current_user
        )

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Ошибка при создании записи"

    return render_template('create.html')

# with app.app_context():
#     db.drop_all()
#     db.create_all()

@app.route('/post/<int:post_id>/comments', methods=['GET', 'POST'])
@login_required
def post_comments(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        comment_text = request.form.get('comment_text')
        if comment_text:
            new_comment = Comment(
                text=comment_text,
                author=current_user,
                post=post
            )
            db.session.add(new_comment)
            db.session.commit()

    return render_template('comments.html', post=post)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=80)
