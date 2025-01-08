import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

# Load .env file
load_dotenv()

api_key = os.getenv("API_KEY")
url_auth = os.getenv("URL_AUTH")
MOVIE_SEARCH_URL = os.getenv("MOVIE_SEARCH_URL")
MOVIE_DETAILS_URL = os.getenv("MOVIE_DETAILS_URL")
IMG_DB_URL = os.getenv("IMG_DB_URL")
headers = {
            'accept': 'application/json',
            'Authorization': os.getenv("AUTH_BEARER_TOKEN")
        }


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


# CREATE EXTENSION
db = SQLAlchemy(model_class=Base)
# instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
# initialize the app with the extension
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()


# CREATE FORM FOR RATING USING WTFORMS
class RateMovieForm(FlaskForm):
    rating = StringField('Your Rating Out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Done')


# CREATE FORM FOR ADD MOVIE USING WTFORMS
class AddForm(FlaskForm):
    add_movie = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


@app.route("/")
def home():
    # READ ALL RECORDS ON THE DATABASE
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_record = result.scalars().all()
    # TURN YOUR DATA INTO A PYTHON LIST.
    for i in range(len(all_record)):
        all_record[i].ranking = len(all_record) - i
    return render_template("index.html", movies=all_record)


# IF USING WTFORMS DONT USE POST METHOD USE VALIDATE ON SUBMIT INSTEAD.
@app.route("/edit", methods=["POST", "GET"])
def edit():
    """ PASS THE ID HERE TO FIGURE OUT WHAT MOVIE WILL BE EDITED"""
    # CREATE AN INSTANCE FROM THE EDITFORM CLASS
    form = RateMovieForm()
    movie_id = request.args.get('id')
    movie_to_update = db.get_or_404(Movie, movie_id)  # This will get the entire row using id.
    if form.validate_on_submit():
        new_rating = form.rating.data
        new_review = form.review.data
        movie_to_update.rating = new_rating
        movie_to_update.review = new_review
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form, movie=movie_to_update)


# DELETE A ROW USING ID
@app.route('/delete')
def delete():
    """This will delete the entire movie details from the database"""
    movie_id = request.args.get('id')
    movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=["POST", "GET"])
def add():
    """This will add a movie to the database"""
    form = AddForm()
    if form.validate_on_submit():
        movie_title = form.add_movie.data
        parameters = {
            "query": movie_title,
            "api_key": api_key
        }
        response = requests.get(MOVIE_SEARCH_URL, headers=headers, params=parameters)
        movie_data = response.json()['results']  # these movie_data are a list of dictionaries
        # print(movie_data)
        return render_template('select.html', movies=movie_data)
    return render_template('add.html', form=form)


# @app.route('/select')
# def select():
#     return render_template('select.html')


@app.route('/find')
def find():
    """This function will find the movie targeted and redirect it to the EDIT ROUTE"""
    movie_id = request.args.get('id')
    if movie_id:
        # API
        url_data_movie = f"{MOVIE_DETAILS_URL}{movie_id}"
        response = requests.get(url_data_movie, headers=headers, params={'api_key': api_key, 'language': "en-US"})
        movie_details = response.json()
        # print(movie_details)
        # ADD TO THE DATABASE
        new_title = movie_details['title']
        new_img_url = f"{IMG_DB_URL}{movie_details['poster_path']}"
        new_year = movie_details['release_date'].split('-')[0]  # This will return year only
        new_description = movie_details['overview']
        new_ranking = 0
        new_rating = 0
        new_review = 'write some'
        new_movie = Movie(title=new_title,
                          year=new_year,
                          description=new_description,
                          img_url=new_img_url,
                          ranking=new_ranking,
                          review=new_review,
                          rating=new_rating)
        db.session.add(new_movie)
        db.session.commit()

        # REDIRECT TO EDIT ROUTE TO EDIT SOME DETAILS TO THE MOVIE
        # PASS THE ID OF THE MOVIE SINCE THE EDIT ROUTE WILL CATCH THAT ID --
        # -- TO FIGURE OUT WHAT MOVIE IS GOING TO BE EDITED FROM THE DATABASE.
        return redirect(url_for('edit', id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
