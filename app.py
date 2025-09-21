from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Movie/Series Model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(50))
    rating = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'rating': self.rating,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Create database tables
with app.app_context():
    db.create_all()

# Base route
@app.route("/")
def hello_world():
    return "<p>Welcome to Movies Tracker!</p>"

# GET all movies
@app.route("/movies", methods=["GET"])
def get_movies():
    movies = Movie.query.all()
    return jsonify([m.to_dict() for m in movies])

# POST new movie
@app.route("/movies", methods=["POST"])
def add_movie():
    data = request.get_json()
    title = data.get("title")
    genre = data.get("genre")
    rating = data.get("rating")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    movie = Movie(title=title, genre=genre, rating=rating)
    db.session.add(movie)
    db.session.commit()
    return jsonify(movie.to_dict()), 201

# PUT update movie
@app.route("/movies/<int:id>", methods=["PUT"])
def create_or_update_movie(id):
    data = request.get_json()
    movie = Movie.query.get(id)
    if not movie:
        movie = Movie(id=id)  # create with specific ID
    movie.title = data["title"]
    movie.genre = data["genre"]
    movie.rating = data["rating"]
    db.session.add(movie)
    db.session.commit()
    return jsonify(movie.to_dict())

# DELETE a movie
@app.route("/movies/<int:id>", methods=["DELETE"])
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Movie deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
