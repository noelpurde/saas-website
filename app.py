from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    first_name = "John"
    stuff = "This is <strong> Bold </strong> Text"
    return render_template("index.html", first_name=first_name, stuff=stuff)

# localhost:500/user/Noel
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)


#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500