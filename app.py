from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

moviemat = pd.read_csv("movie_similarity_pivot.csv", index_col=0)

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')

@app.route("/recms", methods = ["POST"])
def make_rec():
  if request.method == "POST":
        data = request.get_json()
        movie = data["movie_title"]
        rating_series=moviemat[movie]
        #curl -X POST http://192.168.1.10:80/recms -H "Content-Type: application/json" -d "{\"movie_title\":\"Pirates of the Caribbean: The Curse of the Black Pearl (2003)\"}"
        try: 
            similar_to_chosen = moviemat.corrwith(rating_series)
            recommendations = pd.DataFrame(similar_to_chosen,columns=['Correlation'])
            recommendations.dropna(inplace=True)
            api_recommendations = recommendations.sort_values('Correlation',ascending=False).head(10).index.to_list()
        except:
            api_recommendations = ['Movie not found']
        return {"rec_movie":api_recommendations}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)