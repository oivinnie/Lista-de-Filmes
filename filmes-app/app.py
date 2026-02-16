from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    # Lendo os arquivos
    movies = pd.read_csv("movies.csv")
    ratings = pd.read_csv("ratings.csv")

    # Cruzando pelo movieId
    merged = pd.merge(ratings, movies, on="movieId")

    # Calculando média e quantidade de avaliações
    stats = (
        merged
        .groupby("title")
        .agg(
            media=("rating", "mean"),
            total_avaliacoes=("rating", "count")
        )
        .reset_index()
    )

    # Ordenando pelos mais bem avaliados com mínimo de avaliações
    stats = stats[stats["total_avaliacoes"] > 50]
    top = stats.sort_values(by="media", ascending=False).head(20)

    return render_template("index.html", movies=top.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
