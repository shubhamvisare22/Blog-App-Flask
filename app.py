from flask import Flask, render_template, request, flash, redirect
from flask_login import LoginManager, login_user, logout_user, current_user
from models import db, User, Blog
import config

# >>>>>>>>>>>>>>>>>>>>>>>>>>> Configurations >>>>>>>>>>>>>>>>>>>>>>>>>>>
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
app.config['SECRET_KEY'] = config.SECRET_KEY
db.init_app(app)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>> Auth Views >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method != "POST":
        return render_template("register.html")

    try:
        username = request.form.get("userName")
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        passwd = request.form.get("passwd")

        user = User(username=username, email=email,
                    first_name=first_name, last_name=last_name, password=passwd)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully.', 'success')
        return redirect("/login")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect("/register")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method != "POST":
        return render_template("login.html")

    try:
        username = request.form.get("userName")
        passwd = request.form.get("passwd")

        user = User.query.filter_by(username=username).first()

        if user and user.password == passwd:
            login_user(user=user)
            flash(f"Welcome, {user.first_name}!", "success")
            return redirect("/")
        else:
            flash("Invalid credentials.", "warning")
            return redirect("/login")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect("/login")


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')

# >>>>>>>>>>>>>>>>>>>>>>>>>>>> Blog Views >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


@app.route('/', methods=['GET'])
def list_blogs():
    author = request.args.get('user_id', current_user.id)
    blog_list = Blog.query.filter_by(author=int(author)).all()

    if blog_list:
        return render_template("home.html", blogs=blog_list)
    return render_template("home.html")


@app.route('/create', methods=['GET', 'POST'])
def crate_blog():
    if request.method != 'POST':
        return render_template('create_blog.html')

    try:
        title = request.form.get("bg_title")
        content = request.form.get("bg_content")
        author = request.form.get("user_id")

        if title != "" and content != "" and author:
            blog_obj = Blog(title=title, content=content, author=int(author))
            db.session.add(blog_obj)
            db.session.commit()
            flash('Blog posted successfully.', 'success')
            return redirect("/")
        flash('Please enter title and content.', 'danger')
        return redirect("/create")

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect("/login")


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_blogs(id):
    try:
        blog_obj = Blog.query.get(id)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect("/")

    if request.method != "POST":
        return render_template("edit_blog.html", blog=blog_obj)

    try:
        title = request.form.get("bg_title")
        content = request.form.get("bg_content")
        blog_obj.title = title
        blog_obj.content = content
        db.session.commit()
        flash('Blog updated successfully.', 'success')
        return redirect("/")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect("/")


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_blogs(id):
    try:
        blog_obj = Blog.query.get(id)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect("/")

    try:
        if blog_obj:
            db.session.delete(blog_obj)
            db.session.commit()
            flash('Blog deleted successfully.', 'success')
            return redirect("/")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect("/")


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> RUN >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    #     user_obj = Blog.query.all()
    #     print(user_obj)

    app.run(debug=True, port=8000)
