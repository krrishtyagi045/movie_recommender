from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

movies = pd.read_csv("movies.csv")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def recommend():
    genre = request.form['genre']
    language = request.form['language']

    filtered = movies[
        (movies['genre'].str.lower() == genre.lower()) &
        (movies['language'].str.lower() == language.lower())
    ]

    if filtered.empty:
        result = ["No movies found"]
    else:
        result = filtered['title'].tolist()

    return render_template("result.html", movies=result)

if __name__ == "__main__":
    app.run(debug=True)